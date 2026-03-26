# Weather API Specification

## Base URL
https://api.weather.com/v1

## Endpoints

### Get Current Weather
**GET** `/current`

**Query Parameters:**
- `location` (required): City name or coordinates.
- `units` (optional): `metric` or `imperial`. Default is `metric`.

**Authentication:**
API Key required in the `X-API-Key` header.

**Response Example:**
```json
{
  "location": "San Francisco",
  "temperature": 18,
  "condition": "Partly Cloudy",
  "timestamp": "2024-03-26T12:00:00Z"
}
```
