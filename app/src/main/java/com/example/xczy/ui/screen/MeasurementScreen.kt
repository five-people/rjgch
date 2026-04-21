package com.example.xczy.ui.screen

import androidx.compose.foundation.background
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.verticalScroll
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp

/**
 * 测量页面 - 显示GPS定位和坐标信息
 */
@Composable
fun MeasurementScreen(modifier: Modifier = Modifier) {
    var isLocating by remember { mutableStateOf(false) }
    var latitude by remember { mutableStateOf(0.0) }
    var longitude by remember { mutableStateOf(0.0) }
    var projectX by remember { mutableStateOf(0.0) }
    var projectY by remember { mutableStateOf(0.0) }
    var elevation by remember { mutableStateOf(0.0) }
    var accuracy by remember { mutableStateOf(0.0f) }

    Column(
        modifier = modifier
            .fillMaxSize()
            .background(Color.White)
            .verticalScroll(rememberScrollState())
            .padding(16.dp)
    ) {
        // 定位状态卡片
        Card(
            modifier = Modifier
                .fillMaxWidth()
                .padding(bottom = 16.dp),
            colors = CardDefaults.cardColors(containerColor = Color(0xFFF5F5F5)),
            elevation = CardDefaults.cardElevation(defaultElevation = 2.dp)
        ) {
            Column(
                modifier = Modifier.padding(16.dp),
                verticalArrangement = Arrangement.spacedBy(12.dp)
            ) {
                Text(
                    "GPS 定位信息",
                    fontSize = 16.sp,
                    fontWeight = FontWeight.Bold,
                    color = Color.Black
                )

                Row(
                    modifier = Modifier
                        .fillMaxWidth()
                        .background(Color.White, shape = MaterialTheme.shapes.small)
                        .padding(12.dp),
                    horizontalArrangement = Arrangement.SpaceBetween
                ) {
                    Column {
                        Text("纬度", fontSize = 12.sp, color = Color.Gray)
                        Text(
                            "%.6f".format(latitude),
                            fontSize = 14.sp,
                            fontWeight = FontWeight.SemiBold,
                            color = Color.Black
                        )
                    }
                    Column {
                        Text("精度", fontSize = 12.sp, color = Color.Gray)
                        Text(
                            "%.1f m".format(accuracy),
                            fontSize = 14.sp,
                            fontWeight = FontWeight.SemiBold,
                            color = if (accuracy < 5) Color(0xFF4CAF50) else Color(0xFFFF9800)
                        )
                    }
                }

                Row(
                    modifier = Modifier
                        .fillMaxWidth()
                        .background(Color.White, shape = MaterialTheme.shapes.small)
                        .padding(12.dp),
                    horizontalArrangement = Arrangement.SpaceBetween
                ) {
                    Column {
                        Text("经度", fontSize = 12.sp, color = Color.Gray)
                        Text(
                            "%.6f".format(longitude),
                            fontSize = 14.sp,
                            fontWeight = FontWeight.SemiBold,
                            color = Color.Black
                        )
                    }
                    Column {
                        Text("海拔", fontSize = 12.sp, color = Color.Gray)
                        Text(
                            "%.1f m".format(elevation),
                            fontSize = 14.sp,
                            fontWeight = FontWeight.SemiBold,
                            color = Color.Black
                        )
                    }
                }
            }
        }

        // 项目坐标卡片
        Card(
            modifier = Modifier
                .fillMaxWidth()
                .padding(bottom = 16.dp),
            colors = CardDefaults.cardColors(containerColor = Color(0xFFF5F5F5)),
            elevation = CardDefaults.cardElevation(defaultElevation = 2.dp)
        ) {
            Column(
                modifier = Modifier.padding(16.dp),
                verticalArrangement = Arrangement.spacedBy(12.dp)
            ) {
                Text(
                    "项目坐标",
                    fontSize = 16.sp,
                    fontWeight = FontWeight.Bold,
                    color = Color.Black
                )

                Row(
                    modifier = Modifier
                        .fillMaxWidth()
                        .background(Color.White, shape = MaterialTheme.shapes.small)
                        .padding(12.dp),
                    horizontalArrangement = Arrangement.SpaceBetween
                ) {
                    Column {
                        Text("X坐标", fontSize = 12.sp, color = Color.Gray)
                        Text(
                            "%.2f m".format(projectX),
                            fontSize = 14.sp,
                            fontWeight = FontWeight.SemiBold,
                            color = Color.Black
                        )
                    }
                    Column {
                        Text("Y坐标", fontSize = 12.sp, color = Color.Gray)
                        Text(
                            "%.2f m".format(projectY),
                            fontSize = 14.sp,
                            fontWeight = FontWeight.SemiBold,
                            color = Color.Black
                        )
                    }
                }

                Text(
                    "坐标自动转换完成",
                    fontSize = 12.sp,
                    color = Color(0xFF4CAF50),
                    modifier = Modifier.align(Alignment.CenterHorizontally)
                )
            }
        }

        // 操作按钮
        Button(
            onClick = { isLocating = !isLocating },
            modifier = Modifier
                .fillMaxWidth()
                .height(56.dp)
                .padding(bottom = 8.dp),
            colors = ButtonDefaults.buttonColors(
                containerColor = Color(0xFF2196F3),
                contentColor = Color.White
            ),
            shape = MaterialTheme.shapes.medium
        ) {
            Text(
                if (isLocating) "停止定位" else "开始定位",
                fontSize = 16.sp,
                fontWeight = FontWeight.Bold
            )
        }


        Button(
            onClick = {
                // 刷新坐标
                latitude = 39.9 + kotlin.random.Random.nextDouble(-0.01, 0.01)
                longitude = 116.4 + kotlin.random.Random.nextDouble(-0.01, 0.01)
                projectX = 1000 + kotlin.random.Random.nextDouble(-50.0, 50.0)
                projectY = 2000 + kotlin.random.Random.nextDouble(-50.0, 50.0)
                elevation = 50 + kotlin.random.Random.nextDouble(-5.0, 5.0)
                accuracy = 2.5f + kotlin.random.Random.nextFloat()
            },
            modifier = Modifier
                .fillMaxWidth()
                .height(56.dp),
            colors = ButtonDefaults.buttonColors(
                containerColor = Color(0xFF4CAF50),
                contentColor = Color.White
            ),
            shape = MaterialTheme.shapes.medium
        ) {
            Text(
                "刷新数据",
                fontSize = 16.sp,
                fontWeight = FontWeight.Bold
            )
        }
    }
}
