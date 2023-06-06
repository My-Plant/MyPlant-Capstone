
import android.content.Intent
import android.graphics.Color
import android.graphics.drawable.ColorDrawable
import android.os.Bundle
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import android.view.WindowManager
import androidx.appcompat.app.AppCompatActivity
import androidx.fragment.app.Fragment
import com.example.kepston.DaftarPenyakitActivity
import com.example.kepston.DetectFragment
import com.example.kepston.R
import com.example.kepston.databinding.FragmentHomeBinding

class HomeFragment : Fragment(){

    private lateinit var binding: FragmentHomeBinding

    override fun onCreateView(
        inflater: LayoutInflater,
        container: ViewGroup?,
        savedInstanceState: Bundle?
    ): View? {
        binding = FragmentHomeBinding.inflate(inflater, container, false)
        return binding.root
    }

    override fun onViewCreated(view: View, savedInstanceState: Bundle?) {
        super.onViewCreated(view, savedInstanceState)

        (activity as AppCompatActivity).supportActionBar?.setBackgroundDrawable(
            ColorDrawable(
                Color.parseColor(
                    "#91A373"
                )
            )
        )

        activity?.window?.setFlags(
            WindowManager.LayoutParams.FLAG_FULLSCREEN,
            WindowManager.LayoutParams.FLAG_FULLSCREEN
        )


        binding.listplant.setOnClickListener {
            activity?.let {
                openNewActivity()
            }
        }
        binding.detect.setOnClickListener {
            parentFragmentManager.beginTransaction()
                .replace(R.id.fragment_container, DetectFragment())
                .addToBackStack(null)
                .commit()
        }
    }

    private fun openNewActivity() {
        val intent = Intent(activity, DaftarPenyakitActivity::class.java)
        startActivity(intent)
    }
}
