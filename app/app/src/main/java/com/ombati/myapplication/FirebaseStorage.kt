package com.ombati.myapplication

import android.net.Uri
import com.google.firebase.storage.FirebaseStorage
import kotlinx.coroutines.flow.Flow
import kotlinx.coroutines.flow.flow
import kotlinx.coroutines.tasks.await

class FirebaseStorage {

    private val fbStorage = FirebaseStorage.getInstance()

    private val storageRef = fbStorage.reference

    suspend fun uploadImage(
        course:String,
        imageUri: Uri,
    ): Flow<Result<Uri?>> = flow {
        val imageRef = storageRef.child("${course.uppercase().trim()}/${imageUri.lastPathSegment}")
        try {
            val uploadTask = imageRef.putFile(imageUri).await()
            val downloadUrl = uploadTask.storage.downloadUrl.await()
            emit(Result.Success(downloadUrl))
        } catch (e: Exception) {
            e.printStackTrace()
            emit(Result.Error(e.message))
        }
    }
}
