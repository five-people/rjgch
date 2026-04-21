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
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.foundation.Canvas
import androidx.compose.foundation.BorderStroke
import androidx.compose.ui.draw.alpha
/**
 * AR视图页面 - 增强现实实景叠加显示
 */
@Composable
fun ARViewScreen(modifier: Modifier = Modifier) {
    var isAREnabled by remember { mutableStateOf(true) }
    var showGridLines by remember { mutableStateOf(true) }
    var modelOpacity by remember { mutableStateOf(0.8f) }
    var deviationAlert by remember { mutableStateOf(false) }

    Column(
        modifier = modifier
            .fillMaxSize()
            .background(Color.Black)
    ) {
        // AR 视图区域
        Box(
            modifier = Modifier
                .weight(1f)
                .fillMaxWidth()
                .background(Color(0xFF1A1A1A))
        ) {
            // 模拟AR相机视图
            Column(
                modifier = Modifier
                    .fillMaxSize()
                    .align(Alignment.Center),
                verticalArrangement = Arrangement.Center,
                horizontalAlignment = Alignment.CenterHorizontally
            ) {
                // AR 实景叠加区域
                Card(
                    modifier = Modifier
                        .fillMaxWidth(0.9f)
                        .aspectRatio(1f),
                    colors = CardDefaults.cardColors(containerColor = Color(0xFF2A2A2A)),
                    border = BorderStroke(2.dp, Color.Green)
                ) {
                    Box(
                        modifier = Modifier.fillMaxSize(),
                        contentAlignment = Alignment.Center
                    ) {
                        // 网格线
                        if (showGridLines) {
                            Canvas(modifier = Modifier.fillMaxSize()) {
                                val step = size.width / 4
                                for (i in 1..3) {
                                    val x = step * i
                                    drawLine(
                                        color = Color.Green.copy(alpha = 0.3f),
                                        start = androidx.compose.ui.geometry.Offset(x, 0f),
                                        end = androidx.compose.ui.geometry.Offset(x, size.height),
                                        strokeWidth = 1f
                                    )
                                    val y = step * i
                                    drawLine(
                                        color = Color.Green.copy(alpha = 0.3f),
                                        start = androidx.compose.ui.geometry.Offset(0f, y),
                                        end = androidx.compose.ui.geometry.Offset(size.width, y),
                                        strokeWidth = 1f
                                    )
                                }
                            }
                        }

                        // 3D模型叠加区域
                        Column(
                            horizontalAlignment = Alignment.CenterHorizontally,
                            verticalArrangement = Arrangement.Center
                        ) {
                            Text(
                                "🏗️",
                                fontSize = 48.sp,
                                modifier = Modifier.alpha(modelOpacity)
                            )

                            if (deviationAlert) {
                                Card(
                                    modifier = Modifier
                                        .padding(top = 16.dp)
                                        .background(Color(0xFFFF6B6B), shape = MaterialTheme.shapes.small),
                                    colors = CardDefaults.cardColors(containerColor = Color(0xFFFF6B6B))
                                ) {
                                    Text(
                                        "偏差超标警告",
                                        color = Color.White,
                                        fontSize = 14.sp,
                                        fontWeight = FontWeight.Bold,
                                        modifier = Modifier.padding(8.dp)
                                    )
                                }
                            } else {
                                Text(
                                    "正常状态",
                                    color = Color(0xFF4CAF50),
                                    fontSize = 12.sp
                                )
                            }
                        }
                    }
                }

                // 坐标显示
                Row(
                    modifier = Modifier
                        .fillMaxWidth(0.9f)
                        .padding(top = 12.dp)
                        .background(Color(0xFF2A2A2A), shape = MaterialTheme.shapes.small)
                        .padding(12.dp),
                    horizontalArrangement = Arrangement.SpaceAround
                ) {
                    Text("X: 1024.5m", color = Color.Green, fontSize = 12.sp)
                    Text("Y: 2048.3m", color = Color.Green, fontSize = 12.sp)
                    Text("Z: 45.2m", color = Color.Green, fontSize = 12.sp)
                }
            }
        }

        // 控制面板
        Card(
            modifier = Modifier
                .fillMaxWidth()
                .background(Color.Black),
            colors = CardDefaults.cardColors(containerColor = Color(0xFF1A1A1A)),
            shape = RoundedCornerShape(topStart = 16.dp, topEnd = 16.dp)
        ) {
            Column(
                modifier = Modifier
                    .fillMaxWidth()
                    .padding(16.dp)
                    .verticalScroll(rememberScrollState()),
                verticalArrangement = Arrangement.spacedBy(12.dp)
            ) {
                // 模型透明度控制
                Row(
                    modifier = Modifier.fillMaxWidth(),
                    verticalAlignment = Alignment.CenterVertically,
                    horizontalArrangement = Arrangement.SpaceBetween
                ) {
                    Text("模型透明度", color = Color.White, fontSize = 14.sp)
                    Slider(
                        value = modelOpacity,
                        onValueChange = { modelOpacity = it },
                        modifier = Modifier
                            .weight(1f)
                            .padding(start = 12.dp),
                        valueRange = 0f..1f,
                        colors = SliderDefaults.colors(
                            thumbColor = Color(0xFF2196F3),
                            activeTrackColor = Color(0xFF2196F3)
                        )
                    )
                }

                // 功能开关
                Row(
                    modifier = Modifier
                        .fillMaxWidth()
                        .background(Color(0xFF2A2A2A), shape = MaterialTheme.shapes.small)
                        .padding(12.dp),
                    verticalAlignment = Alignment.CenterVertically,
                    horizontalArrangement = Arrangement.SpaceBetween
                ) {
                    Text("网格辅助线", color = Color.White, fontSize = 14.sp)
                    Switch(
                        checked = showGridLines,
                        onCheckedChange = { showGridLines = it },
                        colors = SwitchDefaults.colors(
                            checkedThumbColor = Color(0xFF2196F3),
                            checkedTrackColor = Color(0xFF90CAF9)
                        )
                    )
                }

                Row(
                    modifier = Modifier
                        .fillMaxWidth()
                        .background(Color(0xFF2A2A2A), shape = MaterialTheme.shapes.small)
                        .padding(12.dp),
                    verticalAlignment = Alignment.CenterVertically,
                    horizontalArrangement = Arrangement.SpaceBetween
                ) {
                    Text("偏差检测", color = Color.White, fontSize = 14.sp)
                    Switch(
                        checked = deviationAlert,
                        onCheckedChange = { deviationAlert = it },
                        colors = SwitchDefaults.colors(
                            checkedThumbColor = Color(0xFFFF6B6B),
                            checkedTrackColor = Color(0xFFFFAB91)
                        )
                    )
                }

                // 操作按钮
                Button(
                    onClick = { },
                    modifier = Modifier
                        .fillMaxWidth()
                        .height(48.dp),
                    colors = ButtonDefaults.buttonColors(containerColor = Color(0xFF2196F3)),
                    shape = MaterialTheme.shapes.medium
                ) {
                    Text(
                        "截图保存",
                        color = Color.White,
                        fontSize = 14.sp,
                        fontWeight = FontWeight.Bold
                    )
                }
            }
        }
    }
}

// 画布绘制辅助
//import androidx.compose.foundation.Canvas
//import androidx.compose.foundation.BorderStroke
//import androidx.compose.ui.draw.alpha
