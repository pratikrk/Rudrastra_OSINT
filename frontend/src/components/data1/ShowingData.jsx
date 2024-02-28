import React, { useState, useEffect } from "react";

function ShowingData() {
  const [data, setData] = useState(null);
  const [phoneNumber, setPhoneNumber] = useState("");
  const [countryCode, setCountryCode] = useState("");

  const handleSubmit = async (event) => {
    event.preventDefault();
    try {
      const response = await fetch("http://127.0.0.1:8000/auth/submit-data/", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          phone_number: phoneNumber,
          country_code: countryCode,
        }),
      });
      const responseData = await response.json();
      setData(responseData);
    } catch (error) {
      console.error("Error fetching data:", error);
    }
  };

  return (
    <div className="container mt-5">
      <div className="row">
        <div className="col-md-6 offset-md-3">
          <form onSubmit={handleSubmit}>
            <div className="mb-3">
              <label htmlFor="phoneNumber" className="form-label">
                Phone Number
              </label>
              <input
                type="text"
                className="form-control"
                id="phoneNumber"
                value={phoneNumber}
                onChange={(e) => setPhoneNumber(e.target.value)}
                required
              />
            </div>
            <div className="mb-3">
              <label htmlFor="countryCode" className="form-label">
                Country Code
              </label>
              <input
                type="text"
                className="form-control"
                id="countryCode"
                value={countryCode}
                onChange={(e) => setCountryCode(e.target.value)}
                required
              />
            </div>
            <button type="submit" className="btn btn-primary">
              Submit
            </button>
          </form>
        </div>
      </div>
      {data && (
        <div className="row mt-5">
          <div className="col-md-6 offset-md-3">
            <h2>Phone Lookup</h2>
            <p>Query: {data.phone_lookup.query}</p>
            <p>Status: {data.phone_lookup.status}</p>
            <p>Number Type: {data.phone_lookup.numberType}</p>
            <h2>Breach Data</h2>
            {data.breach_data1.errors[0] === "false" ? (
              <p>No breaches found</p>
            ) : (
              <p>Error: {data.breach_data1.errors[0]}</p>
            )}
          </div>
        </div>
      )}
    </div>
  );
}

export default ShowingData;
