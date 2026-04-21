package com.example.xczy.ui.screen

import androidx.compose.foundation.background
import androidx.compose.foundation.clickable
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
import androidx.compose.material3.Badge
import androidx.compose.material3.Divider
import androidx.compose.foundation.BorderStroke
import androidx.compose.material3.Button
import androidx.compose.material3.ButtonDefaults
/**
 * 我的页面 - 用户个人信息和设置
 */
@Composable
fun ProfileScreen(modifier: Modifier = Modifier) {
    var isOnlineMode by remember { mutableStateOf(true) }
    var enableNotifications by remember { mutableStateOf(true) }
    var autoCalibration by remember { mutableStateOf(true) }

    Column(
        modifier = modifier
            .fillMaxSize()
            .background(Color.White)
            .verticalScroll(rememberScrollState())
    ) {
        // 用户信息卡片
        Card(
            modifier = Modifier
                .fillMaxWidth()
                .padding(16.dp),
            colors = CardDefaults.cardColors(containerColor = Color(0xFF2196F3)),
            elevation = CardDefaults.cardElevation(defaultElevation = 4.dp)
        ) {
            Column(
                modifier = Modifier
                    .fillMaxWidth()
                    .padding(24.dp),
                horizontalAlignment = Alignment.CenterHorizontally,
                verticalArrangement = Arrangement.spacedBy(12.dp)
            ) {
                // 头像
                Box(
                    modifier = Modifier
                        .size(80.dp)
                        .background(Color.White, shape = MaterialTheme.shapes.extraLarge),
                    contentAlignment = Alignment.Center
                ) {
                    Text(
                        "👤",
                        fontSize = 40.sp
                    )
                }

                // 用户名
                Text(
                    "工程测量员",
                    fontSize = 20.sp,
                    fontWeight = FontWeight.Bold,
                    color = Color.White
                )

                // 工号和状态
                Row(
                    modifier = Modifier.fillMaxWidth(),
                    horizontalArrangement = Arrangement.Center,
                    verticalAlignment = Alignment.CenterVertically
                ) {
                    Text(
                        "工号: 2026001",
                        fontSize = 12.sp,
                        color = Color(0xFFBBDEFB)
                    )
                    Divider(
                        modifier = Modifier
                            .width(1.dp)
                            .height(14.dp)
                            .padding(horizontal = 8.dp),
                        color = Color(0xFFBBDEFB)
                    )
                    Badge(
                        containerColor = Color(0xFF4CAF50)
                    ) {
                        Text("在线", fontSize = 10.sp, color = Color.White)
                    }
                }

                // 工作统计
                Row(
                    modifier = Modifier
                        .fillMaxWidth()
                        .padding(top = 12.dp),
                    horizontalArrangement = Arrangement.SpaceEvenly
                ) {
                    UserStatItem("项目", "5")
                    UserStatItem("测量", "128")
                    UserStatItem("工时", "42h")
                }
            }
        }

        // 功能设置区域
        Text(
            "功能设置",
            fontSize = 14.sp,
            fontWeight = FontWeight.Bold,
            color = Color.Gray,
            modifier = Modifier.padding(start = 16.dp, top = 24.dp, bottom = 12.dp)
        )

        // 在线/离线模式
        SettingItem(
            icon = "🌐",
            title = "工作模式",
            subtitle = if (isOnlineMode) "在线模式（实时同步）" else "离线模式（本地作业）",
            trailing = {
                Switch(
                    checked = isOnlineMode,
                    onCheckedChange = { isOnlineMode = it },
                    colors = SwitchDefaults.colors(
                        checkedThumbColor = Color(0xFF2196F3),
                        checkedTrackColor = Color(0xFF90CAF9)
                    )
                )
            }
        )

        // 通知提醒
        SettingItem(
            icon = "🔔",
            title = "偏差警告通知",
            subtitle = "超标时实时提醒",
            trailing = {
                Switch(
                    checked = enableNotifications,
                    onCheckedChange = { enableNotifications = it },
                    colors = SwitchDefaults.colors(
                        checkedThumbColor = Color(0xFF2196F3),
                        checkedTrackColor = Color(0xFF90CAF9)
                    )
                )
            }
        )

        // 自动校准
        SettingItem(
            icon = "🔧",
            title = "自动校准",
            subtitle = "每小时自动重新校准坐标",
            trailing = {
                Switch(
                    checked = autoCalibration,
                    onCheckedChange = { autoCalibration = it },
                    colors = SwitchDefaults.colors(
                        checkedThumbColor = Color(0xFF2196F3),
                        checkedTrackColor = Color(0xFF90CAF9)
                    )
                )
            }
        )

        // 系统信息区域
        Text(
            "系统",
            fontSize = 14.sp,
            fontWeight = FontWeight.Bold,
            color = Color.Gray,
            modifier = Modifier.padding(start = 16.dp, top = 24.dp, bottom = 12.dp)
        )

        SettingItem(
            icon = "ℹ️",
            title = "应用版本",
            subtitle = "1.0.0 (Build 2026)"
        )

        SettingItem(
            icon = "💾",
            title = "缓存大小",
            subtitle = "6.5GB",
            trailing = {
                Button(
                    onClick = { },
                    modifier = Modifier.height(32.dp),
                    colors = ButtonDefaults.buttonColors(containerColor = Color(0xFFFF9800)),
                    contentPadding = PaddingValues(horizontal = 12.dp),
                    shape = MaterialTheme.shapes.small
                ) {
                    Text("清理", fontSize = 11.sp)
                }
            }
        )

        SettingItem(
            icon = "⚙️",
            title = "设置",
            subtitle = "应用配置和权限"
        )

        // 操作按钮
        Spacer(modifier = Modifier.height(24.dp))

        Row(
            modifier = Modifier
                .fillMaxWidth()
                .padding(horizontal = 16.dp),
            horizontalArrangement = Arrangement.spacedBy(12.dp)
        ) {
            Button(
                onClick = { },
                modifier = Modifier
                    .weight(1f)
                    .height(56.dp),
                colors = ButtonDefaults.buttonColors(containerColor = Color(0xFF4CAF50)),
                shape = MaterialTheme.shapes.medium
            ) {
                Text("关于我们", fontWeight = FontWeight.Bold)
            }
            Button(
                onClick = { },
                modifier = Modifier
                    .weight(1f)
                    .height(56.dp),
                colors = ButtonDefaults.buttonColors(containerColor = Color(0xFF2196F3)),
                shape = MaterialTheme.shapes.medium
            ) {
                Text("反馈建议", fontWeight = FontWeight.Bold)
            }
        }

        // 退出按钮
        Button(
            onClick = { },
            modifier = Modifier
                .fillMaxWidth()
                .height(56.dp)
                .padding(16.dp)
                .padding(top = 12.dp),
            colors = ButtonDefaults.buttonColors(containerColor = Color(0xFFFF6B6B)),
            shape = MaterialTheme.shapes.medium
        ) {
            Text("退出登录", fontWeight = FontWeight.Bold)
        }

        Spacer(modifier = Modifier.height(16.dp))
    }
}

@Composable
fun UserStatItem(
    label: String,
    value: String
) {
    Column(
        horizontalAlignment = Alignment.CenterHorizontally,
        verticalArrangement = Arrangement.spacedBy(4.dp)
    ) {
        Text(
            value,
            fontSize = 16.sp,
            fontWeight = FontWeight.Bold,
            color = Color.White
        )
        Text(
            label,
            fontSize = 11.sp,
            color = Color(0xFFBBDEFB)
        )
    }
}

@Composable
fun SettingItem(
    icon: String,
    title: String,
    subtitle: String,
    trailing: (@Composable () -> Unit)? = null
) {
    Card(
        modifier = Modifier
            .fillMaxWidth()
            .padding(horizontal = 16.dp, vertical = 8.dp)
            .clickable { }
            .background(Color.White),
        colors = CardDefaults.cardColors(containerColor = Color.White),
        border = BorderStroke(1.dp, Color(0xFFE0E0E0)),
        elevation = CardDefaults.cardElevation(defaultElevation = 0.dp)
    ) {
        Row(
            modifier = Modifier
                .fillMaxWidth()
                .padding(16.dp),
            verticalAlignment = Alignment.CenterVertically,
            horizontalArrangement = Arrangement.SpaceBetween
        ) {
            Row(
                modifier = Modifier.weight(1f),
                verticalAlignment = Alignment.CenterVertically,
                horizontalArrangement = Arrangement.spacedBy(16.dp)
            ) {
                Text(icon, fontSize = 24.sp)
                Column(
                    verticalArrangement = Arrangement.spacedBy(4.dp)
                ) {
                    Text(
                        title,
                        fontSize = 15.sp,
                        fontWeight = FontWeight.SemiBold,
                        color = Color.Black
                    )
                    Text(
                        subtitle,
                        fontSize = 12.sp,
                        color = Color.Gray
                    )
                }
            }

            if (trailing != null) {
                trailing()
            }
        }
    }
}

//import androidx.compose.material3.Badge
//import androidx.compose.material3.Divider
//import androidx.compose.foundation.BorderStroke
//import androidx.compose.material3.Button
//import androidx.compose.material3.ButtonDefaults
