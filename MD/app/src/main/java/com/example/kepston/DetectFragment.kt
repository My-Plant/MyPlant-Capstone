package com.example.kepston

import android.content.Intent
import android.content.Intent.ACTION_GET_CONTENT
import android.content.pm.PackageManager
import android.graphics.BitmapFactory
import android.net.Uri
import android.os.Build
import android.os.Bundle
import android.os.Environment
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import android.view.WindowManager
import android.widget.Toast
import androidx.activity.result.contract.ActivityResultContracts
import androidx.core.app.ActivityCompat
import androidx.core.content.ContextCompat
import androidx.fragment.app.Fragment
import com.example.kepston.api.ApiConfig
import com.example.kepston.api.FileUploadResponse
import com.example.kepston.databinding.FragmentDetectBinding
import com.google.firebase.auth.FirebaseAuth
import okhttp3.MediaType.Companion.toMediaType
import okhttp3.MultipartBody
import okhttp3.RequestBody.Companion.asRequestBody
import retrofit2.Call
import retrofit2.Callback
import retrofit2.Response
import java.io.File
import java.util.*

class DetectFragment : Fragment() {

    private var image_url: String? = null
    private var prediction: String? = null
    private var deskripsi: ArrayList<String>? = null
    private var deskripsi1: String? = null
    private var solusi: ArrayList<String>? = null
    private var solusi1: String? = null

    private var getFile: File? = null

    private lateinit var auth: FirebaseAuth
    private var _binding: FragmentDetectBinding? = null
    private val binding get() = _binding!!

    companion object {
        const val CAMERA_X_RESULT = 200
        private val REQUIRED_PERMISSIONS = arrayOf(android.Manifest.permission.CAMERA)
        private const val REQUEST_CODE_PERMISSIONS = 10
    }

    override fun onCreateView(
        inflater: LayoutInflater,
        container: ViewGroup?,
        savedInstanceState: Bundle?
    ): View {
        _binding = FragmentDetectBinding.inflate(inflater, container, false)
        return binding.root
    }

    override fun onViewCreated(view: View, savedInstanceState: Bundle?) {
        super.onViewCreated(view, savedInstanceState)

        activity?.window?.setFlags(
            WindowManager.LayoutParams.FLAG_FULLSCREEN,
            WindowManager.LayoutParams.FLAG_FULLSCREEN
        )

        if (!allPermissionsGranted()) {
            ActivityCompat.requestPermissions(
                requireActivity(),
                REQUIRED_PERMISSIONS,
                REQUEST_CODE_PERMISSIONS
            )
        }

        auth = FirebaseAuth.getInstance()

        binding.cameraXButton.setOnClickListener { startCameraX() }
        binding.galleryButton.setOnClickListener { startGallery() }
        binding.uploadButton.setOnClickListener { uploadImage() }
    }

    override fun onDestroyView() {
        super.onDestroyView()
        _binding = null
    }

    private fun allPermissionsGranted() = REQUIRED_PERMISSIONS.all {
        ContextCompat.checkSelfPermission(
            requireContext(),
            it
        ) == PackageManager.PERMISSION_GRANTED
    }

    private fun startGallery() {
        val intent = Intent()
        intent.action = ACTION_GET_CONTENT
        intent.type = "image/*"
        val chooser = Intent.createChooser(intent, "Choose a Picture")
        launcherIntentGallery.launch(chooser)
    }

    private fun startCameraX() {
        val intent = Intent(requireContext(), CameraActivity::class.java)
        launcherIntentCameraX.launch(intent)
    }

    private val launcherIntentCameraX =
        registerForActivityResult(ActivityResultContracts.StartActivityForResult()) { result ->
            if (result.resultCode == CAMERA_X_RESULT) {
                val myFile = if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.TIRAMISU) {
                    result.data?.getSerializableExtra("picture", File::class.java)
                } else {
                    @Suppress("DEPRECATION")
                    result.data?.getSerializableExtra("picture")
                } as? File
                val isBackCamera = result.data?.getBooleanExtra("isBackCamera", true) as Boolean
                myFile?.let { file ->
                    rotateFile(file, isBackCamera)

                    val fileName = "my_image_${UUID.randomUUID()}.jpg"

                    val storageDir = requireContext().getExternalFilesDir(Environment.DIRECTORY_PICTURES)
                    val newFile = File(storageDir, fileName)
                    file.renameTo(newFile)

                    getFile = newFile
                    binding.previewImageView.setImageBitmap(BitmapFactory.decodeFile(newFile.path))
                }
            }
        }

    private val launcherIntentGallery =
        registerForActivityResult(ActivityResultContracts.StartActivityForResult()) { result ->
            if (result.resultCode == -1) {
                val selectedImg = result.data?.data as Uri
                selectedImg.let { uri ->
                    val myFile = uriToFile(uri, requireContext())
                    getFile = myFile
                    binding.previewImageView.setImageURI(uri)
                }
            }
        }

    private fun uploadImage() {
        if (getFile != null) {
            val file = getFile as File
            val requestImageFile = file.asRequestBody("image/jpeg".toMediaType())
            val imageMultipart: MultipartBody.Part = MultipartBody.Part.createFormData(
                "file",
                file.name,
                requestImageFile
            )

            val apiService = ApiConfig().getApiService()
            val uploadImageRequest = apiService.uploadImage(imageMultipart)
            uploadImageRequest.enqueue(object : Callback<FileUploadResponse> {
                override fun onResponse(
                    call: Call<FileUploadResponse>,
                    response: Response<FileUploadResponse>
                ) {
                    if (response.isSuccessful) {
                        val responseBody = response.body()
                        if (responseBody != null) {
                            activity?.let{
                                image_url = responseBody.image_url
                                prediction = responseBody.prediction
                                deskripsi = responseBody.deskripsi
                                deskripsi1 = deskripsi!!.joinToString(separator = " ")
                                solusi = responseBody.solusi
                                solusi1 = solusi!!.joinToString(separator = " ")

                                openNewActivity()
                            }
                        }
                    } else {
                        Toast.makeText(requireContext(), response.message(), Toast.LENGTH_SHORT).show()
                    }
                }
                override fun onFailure(call: Call<FileUploadResponse>, t: Throwable) {
                    Toast.makeText(requireContext(), t.message, Toast.LENGTH_SHORT).show()
                }
            })
        } else {
            Toast.makeText(requireContext(), "Silakan masukkan berkas gambar terlebih dahulu.", Toast.LENGTH_SHORT).show()
        }
    }

    private fun openNewActivity() {
        val intent = Intent(activity, HasilActivity::class.java)
        intent.putExtra("image_url", image_url)
        intent.putExtra("prediction", prediction)
        intent.putExtra("deskripsi1", deskripsi1)
        intent.putExtra("solusi1", solusi1)
        startActivity(intent)
    }
}
