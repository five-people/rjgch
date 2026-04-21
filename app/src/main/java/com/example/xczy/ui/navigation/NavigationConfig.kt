package com.example.xczy.ui.navigation

import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.Home
import androidx.compose.material.icons.filled.LocationOn
import androidx.compose.material.icons.filled.CloudSync
import androidx.compose.material.icons.filled.History
import androidx.compose.material.icons.filled.Person
import androidx.compose.ui.graphics.vector.ImageVector

/**
 * 应用导航配置
 */
object NavigationConfig {
    data class NavigationItem(
        val route: String,
        val label: String,
        val icon: ImageVector
    )

    val items = listOf(
        NavigationItem(
            route = "measurement",
            label = "测量",
            icon = Icons.Filled.LocationOn
        ),
        NavigationItem(
            route = "arview",
            label = "AR视图",
            icon = Icons.Filled.Home
        ),
        NavigationItem(
            route = "offline",
            label = "离线管理",
            icon = Icons.Filled.CloudSync
        ),
        NavigationItem(
            route = "records",
            label = "记录",
            icon = Icons.Filled.History
        ),
        NavigationItem(
            route = "profile",
            label = "我的",
            icon = Icons.Filled.Person
        )
    )
}
