package com.ombati.myapplication

import android.net.Uri
import android.os.Bundle
import androidx.activity.compose.setContent
import androidx.appcompat.app.AppCompatActivity
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxHeight
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.size
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.foundation.verticalScroll
import androidx.compose.material3.Button
import androidx.compose.material3.Card
import androidx.compose.material3.CircularProgressIndicator
import androidx.compose.material3.ExperimentalMaterial3Api
import androidx.compose.material3.OutlinedTextField
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.setValue
import androidx.compose.ui.Modifier
import androidx.compose.ui.layout.ContentScale
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.unit.dp
import androidx.core.net.toUri
import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import androidx.lifecycle.viewmodel.compose.viewModel
import coil.compose.AsyncImage
import coil.request.ImageRequest
import kotlinx.coroutines.launch

class DetailsScreen : AppCompatActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        val uri = intent.getStringExtra("file")
        setContent {
            val viewModel: DetailScreenViewModel = viewModel()
            val uiState = viewModel.uiState.value
            DetailsScreen(
                imageUrl = uri ?: "",
                onUnitCourseChange = viewModel::onCourseChange,
                unitCourse = viewModel.unitCourse,
                onButtonClicked = {
                    viewModel.uploadFile(uri?.toUri())
                },
                uiState = uiState,
                onSuccess = {
                    onBackPressed()
                }
            )
        }
    }
}

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun DetailsScreen(
    modifier: Modifier = Modifier,
    imageUrl: String,
    unitCourse: String,
    uiState: UiState,
    onUnitCourseChange: (String) -> Unit,
    onButtonClicked: () -> Unit,
    onSuccess: () -> Unit
) {
    Column(
        modifier = modifier
            .padding(8.dp)
            .fillMaxSize()
            .verticalScroll(rememberScrollState()),
        verticalArrangement = Arrangement.Top,
    ) {
        Card(
            modifier = Modifier
                .fillMaxWidth()
                .height(500.dp)
        ) {
            AsyncImage(
                modifier = Modifier.fillMaxSize(),
                model = ImageRequest.Builder(LocalContext.current).data(imageUrl).build(),
                contentDescription = null,
                contentScale = ContentScale.Crop
            )
        }
        Spacer(modifier = Modifier.height(20.dp))
        Text(text = "Unit Course")
        OutlinedTextField(
            modifier = Modifier.fillMaxWidth(),
            value = unitCourse,
            onValueChange = onUnitCourseChange,
        )
        Spacer(modifier = Modifier.height(20.dp))
        Button(
            modifier = Modifier.fillMaxWidth(),
            shape = RoundedCornerShape(8.dp),
            onClick = onButtonClicked,
            enabled = !uiState.isLoading,
        ) {
            if (uiState.isLoading) {
                CircularProgressIndicator(modifier = Modifier.size(25.dp))
            } else {
                Text(text = "UPLOAD")
            }
        }
        if (uiState.success) {
            onSuccess.invoke()
        }
    }
}

class DetailScreenViewModel() : ViewModel() {

    private val storage = FirebaseStorage()

    var uiState = mutableStateOf(UiState())
        private set

    var unitCourse: String by mutableStateOf("")
    fun onCourseChange(value: String) {
        unitCourse = value
    }

    fun uploadFile(
        imageUrl: Uri?,
    ) {
        uiState.value = uiState.value.copy(
            isLoading = true
        )
        viewModelScope.launch {
            imageUrl?.let { uri ->
                storage.uploadImage(unitCourse, uri).collect { result ->
                    when (result) {
                        is Result.Error -> {
                            uiState.value = uiState.value.copy(
                                isLoading = false,
                                success = false
                            )
                        }

                        is Result.Success -> {
                            uiState.value = uiState.value.copy(
                                isLoading = false,
                                success = true
                            )
                        }
                    }
                }
            }
        }
    }
}


data class UiState(
    val isLoading: Boolean = false,
    val success: Boolean = false
)