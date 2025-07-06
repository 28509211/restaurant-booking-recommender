package com.example.myproject;

import android.annotation.SuppressLint;
import android.content.Intent;
import android.net.Uri;
import android.os.Bundle;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.ImageView;
import android.widget.LinearLayout;
import android.widget.TextView;

import com.bumptech.glide.Glide;
import com.google.android.material.bottomsheet.BottomSheetDialogFragment;

public class StoreInfoBottomSheet extends BottomSheetDialogFragment {

    private static final String ARG_STORE_NAME = "store_name";
    private static final String ARG_STORE_ADDRESS = "store_address";
    private static final String ARG_STORE_PHONE = "store_phone";
    private static final String ARG_STORE_URL = "store_url";
    private static final String ARG_STORE_LAT = "store_lat";
    private static final String ARG_STORE_LNG = "store_lng";

    private String storeName;
    private String storeAddress;
    private String storePhone;
    private String storeUrl;
    private double storeLat;
    private double storeLng;

    public static StoreInfoBottomSheet newInstance(String storeName, String storeAddress, String storePhone, String storeUrl, double storeLat, double storeLng) {
        StoreInfoBottomSheet fragment = new StoreInfoBottomSheet();
        Bundle args = new Bundle();
        args.putString(ARG_STORE_NAME, storeName);
        args.putString(ARG_STORE_ADDRESS, storeAddress);
        args.putString(ARG_STORE_PHONE, storePhone);
        args.putString(ARG_STORE_URL, storeUrl);
        args.putDouble(ARG_STORE_LAT, storeLat);
        args.putDouble(ARG_STORE_LNG, storeLng);
        fragment.setArguments(args);
        return fragment;
    }

    @Override
    public void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        if (getArguments() != null) {
            storeName = getArguments().getString(ARG_STORE_NAME);
            storeAddress = getArguments().getString(ARG_STORE_ADDRESS);
            storePhone = getArguments().getString(ARG_STORE_PHONE);
            storeUrl = getArguments().getString(ARG_STORE_URL);
            storeLat = getArguments().getDouble(ARG_STORE_LAT);
            storeLng = getArguments().getDouble(ARG_STORE_LNG);
        }
    }

    @Override
    public View onCreateView(LayoutInflater inflater, ViewGroup container, Bundle savedInstanceState) {
        View view = inflater.inflate(R.layout.layout_store_info, container, false);
        ImageView storeImageView = view.findViewById(R.id.storeImageView);
        TextView storeNameTextView = view.findViewById(R.id.storeNameTextView);
        TextView storeAddressTextView = view.findViewById(R.id.storeAddressTextView);
        TextView storePhoneTextView = view.findViewById(R.id.storePhoneTextView);
        LinearLayout storeInfoLayout = view.findViewById(R.id.store_info_layout);

        storeNameTextView.setText(storeName);
        storeAddressTextView.setText(storeAddress);
        storePhoneTextView.setText(storePhone);

        if (storeUrl != null && !storeUrl.isEmpty()) {
            Glide.with(this).load(storeUrl).into(storeImageView);
        }

        storeInfoLayout.setOnClickListener(v -> {
            @SuppressLint("DefaultLocale") String uri = String.format("geo:%f,%f?q=%f,%f(%s)", storeLat, storeLng, storeLat, storeLng, storeName);
            Intent intent = new Intent(Intent.ACTION_VIEW, Uri.parse(uri));
            intent.setPackage("com.google.android.apps.maps");
            startActivity(intent);
        });

        return view;
    }
}
