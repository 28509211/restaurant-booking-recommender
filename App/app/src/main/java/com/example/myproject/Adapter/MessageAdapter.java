package com.example.myproject.Adapter;

import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.LinearLayout;
import android.widget.TextView;

import androidx.annotation.NonNull;
import androidx.recyclerview.widget.RecyclerView;

import com.example.myproject.R;

import java.util.List;

public class MessageAdapter extends RecyclerView.Adapter<MessageAdapter.MessageViewHolder> {

    private List<Message> messageList;
    private View.OnClickListener confirmButtonClickListener;

    public MessageAdapter(List<Message> messageList, View.OnClickListener confirmButtonClickListener) {
        this.messageList = messageList;
        this.confirmButtonClickListener = confirmButtonClickListener;
    }

    @Override
    public int getItemViewType(int position) {
        Message message = messageList.get(position);
        return message.isUserMessage() ? 1 : 0;
    }

    @NonNull
    @Override
    public MessageViewHolder onCreateViewHolder(@NonNull ViewGroup parent, int viewType) {
        View view;
        if (viewType == 1) { // 用戶消息
            view = LayoutInflater.from(parent.getContext()).inflate(R.layout.item_message_user, parent, false);
        } else { // 餐廳列表消息
            view = LayoutInflater.from(parent.getContext()).inflate(R.layout.bubble_message_list, parent, false);
        }
        return new MessageViewHolder(view);
    }

    @Override
    public void onBindViewHolder(@NonNull MessageViewHolder holder, int position) {
        Message message = messageList.get(position);

        if (message.isUserMessage()) {
            holder.tvMessage.setText(message.getText());

            if (message.isShowTimestamp()) {
                holder.timestamp.setVisibility(View.VISIBLE);
                holder.timestamp.setText(message.getTimestamp());
            } else {
                holder.timestamp.setVisibility(View.GONE);
            }
        } else {
            // 顯示餐廳列表
            holder.tvMessage.setText(message.getText());

            // 清空列表容器
            holder.listContainer.removeAllViews();

            // 確保 listItems 不為 null
            if (message.getListItems() != null) {
                // 動態添加每個列表項目
                for (String item : message.getListItems()) {
                    View itemView = LayoutInflater.from(holder.listContainer.getContext()).inflate(R.layout.bubble_list_item, holder.listContainer, false);
                    TextView itemText = itemView.findViewById(R.id.item_text);
                    View indicator = itemView.findViewById(R.id.indicator);

                    itemText.setText(item);

                    // 設置指示器顏色
                    if (item.equals(message.getSelectedRestaurant()) && message.isShowIndicator()) {
                        indicator.setBackgroundResource(R.drawable.selected_circle); // 紫色圓點
                    } else {
                        indicator.setBackgroundResource(R.drawable.unselected_circle); // 灰色圓點
                    }

                    // 設置指示器的可見性
                    indicator.setVisibility(message.isShowIndicator() ? View.VISIBLE : View.GONE);

                    // 設置點擊事件
                    itemView.setOnClickListener(v -> {
                        message.setSelectedRestaurant(item);
                        notifyDataSetChanged(); // 通知適配器數據已更改
                    });

                    holder.listContainer.addView(itemView);
                }
            }
        }
    }




    @Override
    public int getItemCount() {
        return messageList.size();
    }

    public static class MessageViewHolder extends RecyclerView.ViewHolder {

        TextView tvMessage;
        TextView timestamp;
        LinearLayout listContainer; // 容納多個列表項目的容器

        public MessageViewHolder(@NonNull View itemView) {
            super(itemView);
            tvMessage = itemView.findViewById(R.id.tv_message);
            timestamp = itemView.findViewById(R.id.tv_timestamp);
            listContainer = itemView.findViewById(R.id.list_container); // 初始化列表容器
        }
    }
}