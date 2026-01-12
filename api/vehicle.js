function cleanText(data) {
  if (typeof data === "string") {
    return data
      .replace(/@\w+/g, "")
      .replace(/https?:\/\/\S+/gi, "")
      .replace(/www\.\S+/gi, "")
      .trim();
  }

  if (Array.isArray(data)) return data.map(cleanText);

  if (typeof data === "object" && data !== null) {
    const obj = {};
    for (const k in data) obj[k] = cleanText(data[k]);
    return obj;
  }

  return data;
}

export default async function handler(req, res) {
  const { rc } = req.query;

  if (!rc) {
    return res.status(400).json({
      success: false,
      message: "RC number required"
    });
  }

  /* ============ API 2 (PRIORITY) ============ */
  try {
    const api2Url = `https://api.x10.network/numapi.php?action=api&key=thunder&test1=${rc}`;
    const api2Res = await fetch(api2Url); // wait fully
    let api2Data = await api2Res.json();

    api2Data = cleanText(api2Data);

    return res.status(200).json({
      source: "api_2",
      data: api2Data
    });

  } catch (api2Err) {

    /* ============ API 1 (FALLBACK) ============ */
    try {
      const api1Url = `https://new-vehicle-api-eosin.vercel.app/vehicle?rc=${rc}`;
      const api1Res = await fetch(api1Url);
      const api1Data = await api1Res.json();

      return res.status(200).json({
        source: "api_1",
        data: api1Data
      });

    } catch {
      return res.status(404).json({
        success: false,
        message: "Both APIs failed"
      });
    }
  }
}
