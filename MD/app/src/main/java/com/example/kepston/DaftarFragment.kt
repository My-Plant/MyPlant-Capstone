package com.example.kepston

import android.content.Intent
import android.graphics.Color
import android.graphics.drawable.ColorDrawable
import android.os.Bundle
import android.view.*
import android.widget.Toast
import androidx.fragment.app.Fragment
import androidx.fragment.app.viewModels
import androidx.appcompat.app.AppCompatActivity
import androidx.appcompat.app.AppCompatDelegate
import androidx.appcompat.widget.SearchView
import androidx.core.view.isVisible
import androidx.recyclerview.widget.GridLayoutManager
import androidx.recyclerview.widget.LinearLayoutManager
import com.example.kepston.PenyakitAdapter
import com.example.kepston.R
import com.example.kepston.api.ApiConfig
import com.example.kepston.api.ApiConfig1
import com.example.kepston.databinding.ActivityDaftarPenyakitBinding
import com.example.kepston.databinding.FragmentDaftarBinding
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.GlobalScope
import kotlinx.coroutines.flow.catch
import kotlinx.coroutines.flow.flow
import kotlinx.coroutines.flow.onCompletion
import kotlinx.coroutines.flow.onStart
import kotlinx.coroutines.launch

class DaftarFragment : Fragment() {

    private lateinit var binding: FragmentDaftarBinding
    private val adapter by lazy {
        PenyakitAdapter {
            Intent(requireContext(), DetailPenyakitActivity::class.java).apply {
                putExtra("id", it.id)
                putExtra("nama2", it.nama)
                putExtra("deskripsi2", it.deskripsi.joinToString(separator = " "))
                putExtra("solusi2", it.solusi.joinToString(separator = " "))
                putExtra("foto2", it.foto)
                startActivity(this)
            }
        }
    }

    override fun onCreateView(
        inflater: LayoutInflater,
        container: ViewGroup?,
        savedInstanceState: Bundle?
    ): View? {
        binding = FragmentDaftarBinding.inflate(inflater, container, false)
        return binding.root
    }

    override fun onViewCreated(view: View, savedInstanceState: Bundle?) {
        super.onViewCreated(view, savedInstanceState)

        (activity as AppCompatActivity).supportActionBar?.setBackgroundDrawable(
            ColorDrawable(
                Color.parseColor(
                    "#B0BD9A"
                )
            )
        )

        binding.recyclerView.setHasFixedSize(true)
        binding.recyclerView.adapter = adapter
        binding.recyclerView.layoutManager = GridLayoutManager(requireContext(), 2)


        GlobalScope.launch(Dispatchers.IO) {
            launch(Dispatchers.Main) {
                flow {
                    val response = ApiConfig1
                        .apiService
                        .getPenyakit()

                    emit(response)
                }.onStart {
                    binding.progressBar.isVisible = true
                }.onCompletion {
                    binding.progressBar.isVisible = false
                }.catch {
                    Toast.makeText(
                        requireContext(), it.message.toString(),
                        Toast.LENGTH_SHORT
                    ).show()
                }.collect {
                    adapter.setData(it)
                }
            }
        }
    }
}
