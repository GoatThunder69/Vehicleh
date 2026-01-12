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

  /* ================= API 1 ================= */
  try {
    const api1Url = `https://new-vehicle-api-eosin.vercel.app/vehicle?rc=${rc}`;
    const r1 = await fetch(api1Url);
    const d1 = await r1.json();

    const validApi1 =
      d1?.registration_number === rc ||
      d1?.["Ownership Details"]?.["Owner Name"];

    if (validApi1) {
      return res.status(200).json({
        source: "api_1",
        data: d1
      });
    }

    throw new Error("API 1 INVALID DATA");

  } catch (e) {
    /* ================= API 2 ================= */
    try {
      const api2Url = `https://api.x10.network/numapi.php?action=api&key=thunder&test1=${rc}`;
      const r2 = await fetch(api2Url);
      let d2 = await r2.json();

      d2 = cleanText(d2);

      return res.status(200).json({
        source: "api_2",
        data: d2
      });

    } catch (err) {
      return res.status(404).json({
        success: false,
        message: "Data not found in both APIs"
      });
    }
  }
    }
