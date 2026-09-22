export const config = {
  runtime: 'edge',
};

export default async function handler(request) {
  // Handle CORS preflight if needed
  if (request.method === 'OPTIONS') {
    return new Response(null, {
      status: 204,
      headers: {
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Methods': 'POST, OPTIONS',
        'Access-Control-Allow-Headers': 'Content-Type'
      }
    });
  }

  if (request.method !== 'POST') {
    return new Response('Method Not Allowed', { status: 405 });
  }

  try {
    const body = await request.json();
    const userAgent = request.headers.get('user-agent') || '';
    const clientIp = request.headers.get('x-forwarded-for') || '';

    const measurementId = process.env.GA4_MEASUREMENT_ID || 'G-9PCEJCPSV2';
    const apiSecret = process.env.GA4_API_SECRET || '';

    // Asynchronously forward to GA4 Measurement Protocol if secret is present
    if (apiSecret) {
      const gaUrl = `https://www.google-analytics.com/mp/collect?api_secret=${apiSecret}&measurement_id=${measurementId}`;
      fetch(gaUrl, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          client_id: body.client_id || 'anonymous_edge_user',
          events: [{
            name: body.event_name || 'page_view',
            params: {
              page_location: body.page_location,
              page_title: body.page_title,
              engagement_time_msec: 100,
              source: 'vercel_edge_proxy'
            }
          }]
        })
      }).catch(() => {});
    }

    // Return instant 204 No Content to the client browser
    return new Response(null, {
      status: 204,
      headers: {
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Methods': 'POST, OPTIONS',
        'Access-Control-Allow-Headers': 'Content-Type'
      }
    });
  } catch (err) {
    return new Response(null, { status: 204 });
  }
}
