package com.example.myproject.ForGoogleMaps;

import org.json.JSONArray;
import org.json.JSONException;
import org.json.JSONObject;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;

public class DataParser {
    private HashMap<String, String> getSingleNearbyPlace(JSONObject googlePlaceJSON) throws JSONException {
        HashMap<String, String> googlePlaceMap = new HashMap<>();
        String NameOfPlace = "-NA-";
        String vicinity = "-NA-";
        String latitude = "";
        String longitude = "";
        String reference = "";

        if (!googlePlaceJSON.isNull("name")) {
            NameOfPlace = googlePlaceJSON.getString("name");
        }
        if (!googlePlaceJSON.isNull("vicinity")) {
            vicinity = googlePlaceJSON.getString("vicinity");
        }

        latitude = googlePlaceJSON.getJSONObject("geometry").getJSONObject("location").getString("lat");
        longitude = googlePlaceJSON.getJSONObject("geometry").getJSONObject("location").getString("lng");
        reference = googlePlaceJSON.getString("reference");

        googlePlaceMap.put("place_name", NameOfPlace);
        googlePlaceMap.put("vicinity", vicinity);
        googlePlaceMap.put("lat", latitude);
        googlePlaceMap.put("lng", longitude);
        googlePlaceMap.put("reference", reference);

        return googlePlaceMap;
    }

    private List<HashMap<String, String>> getAllNearbyPlaces(JSONArray jsonArray) throws JSONException {
        int counter = jsonArray.length();
        List<HashMap<String, String>> nearbyPlacesList = new ArrayList<>();
        HashMap<String, String> nearbyPlaceMap = null;

        for (int i = 0; i < counter; i++) {
            nearbyPlaceMap = getSingleNearbyPlace((JSONObject) jsonArray.get(i));
            nearbyPlacesList.add(nearbyPlaceMap);
        }
        return nearbyPlacesList;
    }

    public List<HashMap<String, String>> parse(String JSONData) throws JSONException {
        JSONArray jsonArray = null;
        JSONObject jsonObject;

        jsonObject = new JSONObject(JSONData);
        jsonArray = jsonObject.getJSONArray("results");

        return getAllNearbyPlaces(jsonArray);
    }
}
