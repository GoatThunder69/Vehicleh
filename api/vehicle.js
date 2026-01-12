function cleanText(data) {
  if (typeof data === "string") {
    return data
      // remove @username
      .replace(/@\w+/g, "")
      // remove links
      .replace(/https?:\/\/\S+/gi, "")
      .replace(/www\.\S+/gi, "")
      .trim();
  }

  if (Array.isArray(data)) {
    return data.map(cleanText);
  }

  if (typeof data === "object" && data !== null) {
    const cleaned = {};
    for (const key in data) {
      cleaned[key] = cleanText(data[key]);
    }
    return cleaned;
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

  try {
    // ---------- API 1 (Priority) ----------
    const api1Url = `https://new-vehicle-api-eosin.vercel.app/vehicle?rc=${rc}`;
    const api1Res = await fetch(api1Url);
    const api1Data = await api1Res.json();

    if (
      api1Data &&
      api1Data.success !== false &&
      Object.keys(api1Data).length > 0
    ) {
      return res.status(200).json({
        source: "api_1",
        data: api1Data
      });
    }

    throw new Error("API 1 Not Found");

  } catch (err) {
    try {
      // ---------- API 2 (Fallback) ----------
      const api2Url = `https://api.x10.network/numapi.php?action=api&key=thunder&test1=${rc}`;
      const api2Res = await fetch(api2Url);
      let api2Data = await api2Res.json();

      // clean unwanted text (@ , links, etc)
      api2Data = cleanText(api2Data);

      return res.status(200).json({
        source: "api_2",
        data: api2Data
      });

    } catch (e) {
      return res.status(404).json({
        success: false,
        message: "Data not found in both APIs"
      });
    }
  }
}
