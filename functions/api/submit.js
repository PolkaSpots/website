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
    return reply(400, { ok: false, error: "unreadable body" });
  }

  // Honeypot: real people leave it empty, bots fill everything in.
  if (data._gotcha) return reply(200, { ok: true });

  const subject = String(data._subject || "Enquiry via polkaspots.com").slice(0, 200);
  delete data._subject;
  delete data._gotcha;

  const fields = Object.entries(data)
    .filter(([, v]) => String(v).trim() !== "")
    .map(([k, v]) => `${k}: ${String(v).slice(0, 2000)}`);

  if (!fields.length) return reply(400, { ok: false, error: "empty submission" });

  const text = fields.join("\n");
  const meta = {
    submitted: new Date().toISOString(),
    page: request.headers.get("referer") || "",
    country: request.headers.get("cf-ipcountry") || "",
  };

  if (env.FORM_WEBHOOK) {
    const res = await fetch(env.FORM_WEBHOOK, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      // `text` suits Slack; the flat fields suit Zapier and Make.
      body: JSON.stringify({ text: `*${subject}*\n${text}`, subject, ...data, ...meta }),
    });
    if (!res.ok) return reply(502, { ok: false, error: "webhook rejected" });
    return reply(200, { ok: true });
  }

  if (env.RESEND_API_KEY) {
    const res = await fetch("https://api.resend.com/emails", {
      method: "POST",
      headers: {
        Authorization: `Bearer ${env.RESEND_API_KEY}`,
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        from: env.FORM_FROM || "forms@polkaspots.com",
        to: env.FORM_TO || "security@polkaspots.com",
        reply_to: data.email || undefined,
        subject,
        text: `${text}\n\n---\nsubmitted: ${meta.submitted}\npage: ${meta.page}\ncountry: ${meta.country}`,
      }),
    });
    if (!res.ok) return reply(502, { ok: false, error: "email provider rejected" });
    return reply(200, { ok: true });
  }

  // Nothing configured — tell the client so it can fall back to the mailto.
  return reply(503, { ok: false, error: "no destination configured" });
}

export async function onRequestGet() {
  return reply(405, { ok: false, error: "post only" });
}
