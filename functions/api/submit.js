/**
 * Form delivery for polkaspots.com — a Cloudflare Pages Function.
 *
 * Accepts a submission and forwards it to whichever destination is configured
 * as an environment variable in the Pages project. Set EITHER:
 *
 *   FORM_WEBHOOK   any webhook URL — a Zapier catch hook, a Make scenario, a
 *                  Slack incoming webhook. A Zapier hook is the quickest route
 *                  to the notification + spreadsheet row the spec asks for.
 *   RESEND_API_KEY a Resend key, if you would rather it just emailed you.
 *                  Optionally set FORM_TO (defaults to security@polkaspots.com)
 *                  and FORM_FROM (defaults to forms@polkaspots.com, which must
 *                  be a verified Resend sender).
 *
 * If neither is set the endpoint returns 503 and the browser falls back to the
 * mailto. That is deliberate: a submission must never be silently swallowed by
 * an unconfigured endpoint.
 */

const CORS = {
  "Content-Type": "application/json",
  "Cache-Control": "no-store",
};

function reply(status, body) {
  return new Response(JSON.stringify(body), { status, headers: CORS });
}

export async function onRequestPost({ request, env }) {
  let data;
  try {
    const ct = request.headers.get("content-type") || "";
    if (ct.includes("application/json")) {
      data = await request.json();
    } else {
      data = Object.fromEntries(await request.formData());
    }
  } catch (err) {
    return reply(200, { ok: false, error: "unreadable body" });
  }

  // Honeypot: real people leave it empty, bots fill everything in.
  if (data._gotcha) return reply(200, { ok: true });

  const subject = String(data._subject || "Enquiry via polkaspots.com").slice(0, 200);
  delete data._subject;
  delete data._gotcha;

  const fields = Object.entries(data)
    .filter(([, v]) => String(v).trim() !== "")
    .map(([k, v]) => `${k}: ${String(v).slice(0, 2000)}`);

  if (!fields.length) return reply(200, { ok: false, error: "empty submission" });

  const text = fields.join("\n");
  const meta = {
    submitted: new Date().toISOString(),
    page: request.headers.get("referer") || "",
    country: request.headers.get("cf-ipcountry") || "",
  };

  // Deliver to EVERY configured destination, not the first one that matches —
  // a Slack ping and an email in the inbox serve different purposes and you
  // usually want both. Runs them concurrently; one bad destination cannot stop
  // another. The submission counts as delivered if at least one succeeds.
  const jobs = [];

  if (env.FORM_WEBHOOK) {
    jobs.push(
      fetch(env.FORM_WEBHOOK, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        // `text` renders in Slack; the flat fields suit Zapier and Make.
        body: JSON.stringify({
          text: `*${subject}*\n${text}\n_${meta.page || "no referrer"}_`,
          subject, ...data, ...meta,
        }),
      })
        .then((r) => ({ name: "webhook", ok: r.ok, status: r.status }))
        .catch((e) => ({ name: "webhook", ok: false, status: 0, detail: String(e).slice(0, 200) }))
    );
  }

  if (env.RESEND_API_KEY) {
    const send = (from) => fetch("https://api.resend.com/emails", {
      method: "POST",
      headers: {
        Authorization: `Bearer ${env.RESEND_API_KEY}`,
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        from,
        to: env.FORM_TO || "security@polkaspots.com",
        reply_to: data.email || undefined,
        subject,
        text: `${text}\n\n---\nsubmitted: ${meta.submitted}\npage: ${meta.page}\ncountry: ${meta.country}`,
      }),
    });

    // Prefer our own domain; fall back to Resend's shared sender only while
    // polkaspots.com is unverified there.
    jobs.push(
      (async () => {
        let r = await send(env.FORM_FROM || "forms@polkaspots.com");
        if (r.status === 403 && !env.FORM_FROM) r = await send("onboarding@resend.dev");
        return { name: "email", ok: r.ok, status: r.status,
                 detail: r.ok ? undefined : (await r.text()).slice(0, 300) };
      })().catch((e) => ({ name: "email", ok: false, status: 0, detail: String(e).slice(0, 200) }))
    );
  }

  if (jobs.length) {
    const results = await Promise.all(jobs);
    const delivered = results.filter((r) => r.ok).map((r) => r.name);
    const failed = results.filter((r) => !r.ok);
    if (delivered.length) {
      return reply(200, { ok: true, delivered, failed: failed.length ? failed : undefined });
    }
    return reply(200, { ok: false, error: "all destinations failed", failed });
  }

  // Everything failed — tell the client so it can fall back to the mailto
  // rather than let a submission disappear.
  return reply(200, { ok: false, error: "no destination configured" });
}

/**
 * GET reports which destinations the Function can actually see. Booleans only —
 * never the values — so it is safe to leave in place. Cloudflare Pages binds
 * environment variables per deployment, so if this says false after you have
 * saved one, check it was saved against Production rather than Preview, then
 * redeploy: existing deployments keep the environment they were created with.
 */
export async function onRequestGet({ env }) {
  return reply(200, {
    ok: true,
    configured: {
      FORM_WEBHOOK: Boolean(env.FORM_WEBHOOK),
      RESEND_API_KEY: Boolean(env.RESEND_API_KEY),
      FORM_TO: env.FORM_TO || "(default) security@polkaspots.com",
      FORM_FROM: env.FORM_FROM || "(default) forms@polkaspots.com",
    },
    visibleKeys: Object.keys(env || {}).sort(),
  });
}
