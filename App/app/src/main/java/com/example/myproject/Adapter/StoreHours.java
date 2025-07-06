package com.example.myproject.Adapter;

import android.os.Parcel;
import android.os.Parcelable;

public class StoreHours implements Parcelable {
    private final String dayOfWeek;
    private final String openTime1;
    private final String closeTime1;
    private final String openTime2;
    private final String closeTime2;

    public StoreHours(String dayOfWeek, String openTime1, String closeTime1, String openTime2, String closeTime2) {
        this.dayOfWeek = dayOfWeek;
        this.openTime1 = openTime1;
        this.closeTime1 = closeTime1;
        this.openTime2 = openTime2;
        this.closeTime2 = closeTime2;
    }

    protected StoreHours(Parcel in) {
        dayOfWeek = in.readString();
        openTime1 = in.readString();
        closeTime1 = in.readString();
        openTime2 = in.readString();
        closeTime2 = in.readString();
    }

    public static final Creator<StoreHours> CREATOR = new Creator<StoreHours>() {
        @Override
        public StoreHours createFromParcel(Parcel in) {
            return new StoreHours(in);
        }

        @Override
        public StoreHours[] newArray(int size) {
            return new StoreHours[size];
        }
    };

    public String getDayOfWeek() {
        return dayOfWeek;
    }

    public String getOpenTime1() {
        return openTime1;
    }

    public String getCloseTime1() {
        return closeTime1;
    }

    public String getOpenTime2() {
        return openTime2;
    }

    public String getCloseTime2() {
        return closeTime2;
    }

    @Override
    public int describeContents() {
        return 0;
    }

    @Override
    public void writeToParcel(Parcel dest, int flags) {
        dest.writeString(dayOfWeek);
        dest.writeString(openTime1);
        dest.writeString(closeTime1);
        dest.writeString(openTime2);
        dest.writeString(closeTime2);
    }
}
