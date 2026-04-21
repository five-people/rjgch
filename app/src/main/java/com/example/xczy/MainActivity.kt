package com.example.xczy

import android.os.Bundle
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.activity.enableEdgeToEdge
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.padding
import androidx.compose.material3.Icon
import androidx.compose.material3.Scaffold
import androidx.compose.material3.Text
import androidx.compose.material3.adaptive.navigationsuite.NavigationSuiteScaffold
import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.saveable.rememberSaveable
import androidx.compose.runtime.setValue
import androidx.compose.ui.Modifier
import androidx.compose.ui.res.painterResource
import androidx.compose.ui.tooling.preview.Preview
import androidx.compose.ui.tooling.preview.PreviewScreenSizes
import com.example.xczy.ui.theme.XczyTheme
import com.example.xczy.ui.screen.MeasurementScreen
import com.example.xczy.ui.screen.ARViewScreen
import com.example.xczy.ui.screen.OfflineManagementScreen
import com.example.xczy.ui.screen.RecordsScreen
import com.example.xczy.ui.screen.ProfileScreen

class MainActivity : ComponentActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        enableEdgeToEdge()
        setContent {
            XczyTheme {
                XczyApp()
            }
        }
    }
}

@PreviewScreenSizes
@Composable
fun XczyApp() {
    var currentDestination by rememberSaveable { mutableStateOf(AppDestinations.MEASUREMENT) }

    NavigationSuiteScaffold(
        navigationSuiteItems = {
            AppDestinations.entries.forEach {
                item(
                    icon = {
                        Icon(
                            painterResource(it.icon),
                            contentDescription = it.label
                        )
                    },
                    label = { Text(it.label) },
                    selected = it == currentDestination,
                    onClick = { currentDestination = it }
                )
            }
        }
    ) {
        Scaffold(modifier = Modifier.fillMaxSize()) { innerPadding ->
            when (currentDestination) {
                AppDestinations.MEASUREMENT -> {
                    MeasurementScreen(modifier = Modifier.padding(innerPadding))
                }
                AppDestinations.AR_VIEW -> {
                    ARViewScreen(modifier = Modifier.padding(innerPadding))
                }
                AppDestinations.OFFLINE -> {
                    OfflineManagementScreen(modifier = Modifier.padding(innerPadding))
                }
                AppDestinations.RECORDS -> {
                    RecordsScreen(modifier = Modifier.padding(innerPadding))
                }
                AppDestinations.PROFILE -> {
                    ProfileScreen(modifier = Modifier.padding(innerPadding))
                }
            }
        }
    }
}

enum class AppDestinations(
    val label: String,
    val icon: Int,
) {
    MEASUREMENT("测量", R.drawable.ic_home),
    AR_VIEW("AR视图", R.drawable.ic_favorite),
    OFFLINE("离线管理", R.drawable.ic_account_box),
    RECORDS("记录", R.drawable.ic_home),
    PROFILE("我的", R.drawable.ic_account_box),
}

@Preview(showBackground = true)
@Composable
fun XczyAppPreview() {
    XczyTheme {
        XczyApp()
    }
}