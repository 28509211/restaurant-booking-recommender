package com.example.myproject;

import android.Manifest;
import android.annotation.SuppressLint;
import android.content.pm.PackageManager;
import android.os.Bundle;
import androidx.annotation.NonNull;
import androidx.annotation.Nullable;
import androidx.core.app.ActivityCompat;
import androidx.core.content.ContextCompat;
import androidx.fragment.app.Fragment;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.Toast;

import com.android.volley.Request;
import com.android.volley.RequestQueue;
import com.android.volley.Response;
import com.android.volley.VolleyError;
import com.android.volley.toolbox.JsonArrayRequest;
import com.android.volley.toolbox.Volley;
import com.google.android.gms.location.FusedLocationProviderClient;
import com.google.android.gms.location.LocationServices;
import com.google.android.gms.maps.CameraUpdateFactory;
import com.google.android.gms.maps.GoogleMap;
import com.google.android.gms.maps.OnMapReadyCallback;
import com.google.android.gms.maps.SupportMapFragment;
import com.google.android.gms.maps.model.BitmapDescriptorFactory;
import com.google.android.gms.maps.model.LatLng;
import com.google.android.gms.maps.model.Marker;
import com.google.android.gms.maps.model.MarkerOptions;

import org.json.JSONArray;
import org.json.JSONException;
import org.json.JSONObject;

public class MapsFragment extends Fragment implements OnMapReadyCallback {

    private GoogleMap mMap;
    private RequestQueue requestQueue;

    private static final int LOCATION_PERMISSION_REQUEST_CODE = 1;

    public MapsFragment() {
        // Required empty public constructor
    }

    @Override
    public void onCreate(@Nullable Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        requestQueue = Volley.newRequestQueue(requireContext());
    }

    @Nullable
    @Override
    public View onCreateView(@NonNull LayoutInflater inflater, @Nullable ViewGroup container, @Nullable Bundle savedInstanceState) {
        return inflater.inflate(R.layout.fragment_maps, container, false);
    }

    @Override
    public void onViewCreated(@NonNull View view, @Nullable Bundle savedInstanceState) {
        super.onViewCreated(view, savedInstanceState);
        SupportMapFragment mapFragment = (SupportMapFragment) getChildFragmentManager().findFragmentById(R.id.map);
        if (mapFragment != null) {
            mapFragment.getMapAsync(this);
        }
    }

    @Override
    public void onMapReady(GoogleMap googleMap) {
        mMap = googleMap;
        // 启用缩放控件和手势
        mMap.getUiSettings().setZoomControlsEnabled(true);
        mMap.getUiSettings().setZoomGesturesEnabled(true);
        checkLocationPermission();
        mMap.setOnMarkerClickListener(new GoogleMap.OnMarkerClickListener() {
            @Override
            public boolean onMarkerClick(Marker marker) {
                StoreInfo storeInfo = (StoreInfo) marker.getTag();
                if (storeInfo != null) {
                    StoreInfoBottomSheet bottomSheet = StoreInfoBottomSheet.newInstance(
                            storeInfo.getName(),
                            storeInfo.getAddress(),
                            storeInfo.getPhone(),
                            storeInfo.getUrl(),
                            marker.getPosition().latitude,
                            marker.getPosition().longitude
                    );
                    bottomSheet.show(getParentFragmentManager(), bottomSheet.getTag());
                }
                return true;
            }
        });
    }

    private void checkLocationPermission() {
        if (ContextCompat.checkSelfPermission(requireContext(), Manifest.permission.ACCESS_FINE_LOCATION)
                == PackageManager.PERMISSION_GRANTED) {
            getUserLocation();
        } else {
            ActivityCompat.requestPermissions(requireActivity(), new String[]{Manifest.permission.ACCESS_FINE_LOCATION},
                    LOCATION_PERMISSION_REQUEST_CODE);
        }
    }

//    @SuppressLint("MissingPermission")
//    private void getUserLocation() {
//        // 设置默认位置的经纬度
//        double defaultLatitude = 24.95746049372835;
//        double defaultLongitude = 121.24076566782693;
//
//        LatLng defaultLatLng = new LatLng(defaultLatitude, defaultLongitude);
//        mMap.addMarker(new MarkerOptions().position(defaultLatLng).title("Default Location")
//                .icon(BitmapDescriptorFactory.defaultMarker(BitmapDescriptorFactory.HUE_AZURE)));
//        mMap.moveCamera(CameraUpdateFactory.newLatLngZoom(defaultLatLng, 15));
//
//        // 直接使用默认位置获取附近的店家
//        fetchNearbyStores(defaultLatitude, defaultLongitude);
//    }

    @SuppressLint("MissingPermission")
    private void getUserLocation() {
        // 使用 requireContext() 獲取 Context
        FusedLocationProviderClient fusedLocationProviderClient = LocationServices.getFusedLocationProviderClient(requireContext());

        // 嘗試獲取使用者的最後已知位置
        fusedLocationProviderClient.getLastLocation().addOnSuccessListener(location -> {
            if (location != null) {
                // 使用獲得的使用者位置
                double userLatitude = location.getLatitude();
                double userLongitude = location.getLongitude();

                LatLng userLatLng = new LatLng(userLatitude, userLongitude);
                mMap.addMarker(new MarkerOptions()
                        .position(userLatLng)
                        .title("Your Location")
                        .icon(BitmapDescriptorFactory.defaultMarker(BitmapDescriptorFactory.HUE_BLUE)));
                mMap.moveCamera(CameraUpdateFactory.newLatLngZoom(userLatLng, 15));

                // 使用使用者位置來獲取附近的店家
                fetchNearbyStores(userLatitude, userLongitude);
            } else {
                // 如果無法獲取使用者位置，使用預設位置
                useDefaultLocation();
            }
        }).addOnFailureListener(e -> {
            // 如果出現錯誤，使用預設位置
            useDefaultLocation();
        });
    }


    private void useDefaultLocation() {
        double defaultLatitude = 24.95746049372835;
        double defaultLongitude = 121.24076566782693;

        LatLng defaultLatLng = new LatLng(defaultLatitude, defaultLongitude);
        mMap.addMarker(new MarkerOptions()
                .position(defaultLatLng)
                .title("Default Location")
                .icon(BitmapDescriptorFactory.defaultMarker(BitmapDescriptorFactory.HUE_AZURE)));
        mMap.moveCamera(CameraUpdateFactory.newLatLngZoom(defaultLatLng, 15));

        // 使用預設位置來獲取附近的店家
        fetchNearbyStores(defaultLatitude, defaultLongitude);
    }

    private void fetchNearbyStores(double lat, double lng) {
        String url = "https://subdomain1.jp.ngrok.io/login-register-android/get_nearby_stores.php?lat=" + lat + "&lng=" + lng;
        JsonArrayRequest jsonArrayRequest = new JsonArrayRequest(Request.Method.GET, url, null,
                new Response.Listener<JSONArray>() {
                    @Override
                    public void onResponse(JSONArray response) {
                        try {
                            for (int i = 0; i < response.length(); i++) {
                                JSONObject store = response.getJSONObject(i);
                                String storeName = store.getString("store_name");
                                double latitude = store.getDouble("latitude");
                                double longitude = store.getDouble("longitude");
                                String address = store.getString("address");
                                String phone = store.getString("phone");
                                String url = store.getString("url");

                                LatLng storeLocation = new LatLng(latitude, longitude);
                                Marker marker = mMap.addMarker(new MarkerOptions().position(storeLocation).title(storeName)
                                        .icon(BitmapDescriptorFactory.defaultMarker(BitmapDescriptorFactory.HUE_VIOLET)));
                                marker.setTag(new StoreInfo(storeName, address, phone, url));
                            }
                        } catch (JSONException e) {
                            e.printStackTrace();
                        }
                    }
                },
                new Response.ErrorListener() {
                    @Override
                    public void onErrorResponse(VolleyError error) {
                        error.printStackTrace();
                    }
                });

        requestQueue.add(jsonArrayRequest);
    }

    @Override
    public void onRequestPermissionsResult(int requestCode, @NonNull String[] permissions, @NonNull int[] grantResults) {
        if (requestCode == LOCATION_PERMISSION_REQUEST_CODE) {
            if (grantResults.length > 0 && grantResults[0] == PackageManager.PERMISSION_GRANTED) {
                getUserLocation();
            } else {
                Toast.makeText(requireContext(), "Permission denied to access your location", Toast.LENGTH_SHORT).show();
            }
        }
    }

    static class StoreInfo {
        private final String name;
        private final String address;
        private final String phone;
        private final String url;

        public StoreInfo(String name, String address, String phone, String url) {
            this.name = name;
            this.address = address;
            this.phone = phone;
            this.url = url;
        }

        public String getName() {
            return name;
        }

        public String getAddress() {
            return address;
        }

        public String getPhone() {
            return phone;
        }

        public String getUrl() {
            return url;
        }
    }
}
