package com.example.kepston

import android.view.LayoutInflater
import android.view.ViewGroup
import androidx.recyclerview.widget.RecyclerView
import coil.load
import coil.transform.CircleCropTransformation
import com.example.kepston.api.PenyakitResponse
import com.example.kepston.databinding.ItemPenyakitBinding

class PenyakitAdapter(
    private val data: MutableList<PenyakitResponse.PenyakitResponseItem> = mutableListOf(),
    private val listener: (PenyakitResponse.PenyakitResponseItem) -> Unit
) :
    RecyclerView.Adapter<PenyakitAdapter.UserViewHolder>() {

    fun setData(data: MutableList<PenyakitResponse.PenyakitResponseItem>) {
        this.data.clear()
        this.data.addAll(data)
        notifyDataSetChanged()
    }

    class UserViewHolder(private val v: ItemPenyakitBinding) : RecyclerView.ViewHolder(v.root) {
        fun bind(item: PenyakitResponse.PenyakitResponseItem){
            v.image.load(item.foto) {
                transformations(CircleCropTransformation())
            }

            v.username.text = item.nama
        }
    }

    override fun onCreateViewHolder(parent: ViewGroup, viewType: Int): UserViewHolder =
        UserViewHolder(ItemPenyakitBinding.inflate(LayoutInflater.from(parent.context), parent, false))

    override fun onBindViewHolder(holder: UserViewHolder, position: Int) {
        val item = data[position]
        holder.bind(item)
        holder.itemView.setOnClickListener {
            listener(item)
        }
    }

    override fun getItemCount(): Int = data.size
}