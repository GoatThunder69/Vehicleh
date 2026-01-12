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
