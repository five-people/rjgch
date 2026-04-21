package com.example.xczy.ui.screen

import androidx.compose.foundation.background
import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import androidx.compose.foundation.BorderStroke
import androidx.compose.material3.Badge
import androidx.compose.material3.Divider
data class ProjectData(
    val id: Int,
    val name: String,
    val size: String,
    val lastSync: String,
    val dataCount: Int,
    val isSync: Boolean = false
)

/**
 * 离线管理页面 - 管理离线数据和项目同步
 */
@Composable
fun OfflineManagementScreen(modifier: Modifier = Modifier) {
    var isSyncing by remember { mutableStateOf(false) }
    var storageUsage by remember { mutableStateOf(0.65f) }
    
    val projectList = remember {
        listOf(
            ProjectData(1, "北京中关村项目", "245MB", "2026-04-20 14:30", 1250, true),
            ProjectData(2, "上海浦东工程", "156MB", "2026-04-19 09:15", 856, true),
            ProjectData(3, "深圳南山施工", "89MB", "2026-04-18 16:45", 412, false)
        )
    }

    Column(
        modifier = modifier
            .fillMaxSize()
            .background(Color.White)
    ) {
        // 顶部统计卡片
        Card(
            modifier = Modifier
                .fillMaxWidth()
                .padding(16.dp),
            colors = CardDefaults.cardColors(containerColor = Color(0xFFF5F5F5)),
            elevation = CardDefaults.cardElevation(defaultElevation = 2.dp)
        ) {
            Column(
                modifier = Modifier
                    .fillMaxWidth()
                    .padding(16.dp),
                verticalArrangement = Arrangement.spacedBy(16.dp)
            ) {
                // 存储容量
                Row(
                    modifier = Modifier
                        .fillMaxWidth(),
                    verticalAlignment = Alignment.CenterVertically,
                    horizontalArrangement = Arrangement.SpaceBetween
                ) {
                    Column {
                        Text("存储使用", fontSize = 14.sp, color = Color.Gray)
                        Text(
                            "${(storageUsage * 100).toInt()}%",
                            fontSize = 20.sp,
                            fontWeight = FontWeight.Bold,
                            color = Color.Black
                        )
                    }
                    Text("6.5GB / 10GB", fontSize = 12.sp, color = Color.Gray)
                }

                LinearProgressIndicator(
                    progress = { storageUsage },
                    modifier = Modifier
                        .fillMaxWidth()
                        .height(8.dp),
                    color = Color(0xFF2196F3),
                    trackColor = Color(0xFFE0E0E0),
                )

                // 同步状态
                Row(
                    modifier = Modifier
                        .fillMaxWidth()
                        .background(Color.White, shape = MaterialTheme.shapes.small)
                        .padding(12.dp),
                    horizontalArrangement = Arrangement.SpaceBetween,
                    verticalAlignment = Alignment.CenterVertically
                ) {
                    Column {
                        Text("上次同步", fontSize = 12.sp, color = Color.Gray)
                        Text(
                            "2026-04-20 14:30",
                            fontSize = 14.sp,
                            fontWeight = FontWeight.SemiBold,
                            color = Color(0xFF4CAF50)
                        )
                    }
                    Button(
                        onClick = { isSyncing = !isSyncing },
                        modifier = Modifier.height(40.dp),
                        colors = ButtonDefaults.buttonColors(
                            containerColor = if (isSyncing) Color(0xFFFF9800) else Color(0xFF2196F3)
                        ),
                        shape = MaterialTheme.shapes.small
                    ) {
                        Text(
                            if (isSyncing) "同步中..." else "立即同步",
                            fontSize = 12.sp
                        )
                    }
                }
            }
        }

        // 项目列表标题
        Text(
            "离线项目",
            fontSize = 16.sp,
            fontWeight = FontWeight.Bold,
            color = Color.Black,
            modifier = Modifier.padding(start = 16.dp, top = 8.dp, bottom = 8.dp)
        )

        // 项目列表
        LazyColumn(
            modifier = Modifier
                .fillMaxWidth()
                .weight(1f)
                .padding(horizontal = 16.dp),
            verticalArrangement = Arrangement.spacedBy(12.dp)
        ) {
            items(projectList) { project ->
                ProjectDataCard(project)
            }
        }

        // 底部操作按钮
        Row(
            modifier = Modifier
                .fillMaxWidth()
                .padding(16.dp),
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
                Text("添加项目", fontWeight = FontWeight.Bold)
            }
            Button(
                onClick = { },
                modifier = Modifier
                    .weight(1f)
                    .height(56.dp),
                colors = ButtonDefaults.buttonColors(containerColor = Color(0xFFFF6B6B)),
                shape = MaterialTheme.shapes.medium
            ) {
                Text("清理缓存", fontWeight = FontWeight.Bold)
            }
        }
    }
}

@Composable
fun ProjectDataCard(project: ProjectData) {
    Card(
        modifier = Modifier
            .fillMaxWidth()
            .clickable { }
            .background(Color.White),
        colors = CardDefaults.cardColors(containerColor = Color(0xFFFAFAFA)),
        border = BorderStroke(1.dp, Color(0xFFE0E0E0)),
        elevation = CardDefaults.cardElevation(defaultElevation = 1.dp)
    ) {
        Column(
            modifier = Modifier
                .fillMaxWidth()
                .padding(16.dp),
            verticalArrangement = Arrangement.spacedBy(8.dp)
        ) {
            // 项目名称和状态
            Row(
                modifier = Modifier.fillMaxWidth(),
                horizontalArrangement = Arrangement.SpaceBetween,
                verticalAlignment = Alignment.CenterVertically
            ) {
                Text(
                    project.name,
                    fontSize = 15.sp,
                    fontWeight = FontWeight.SemiBold,
                    color = Color.Black
                )
                Badge(
                    containerColor = if (project.isSync) Color(0xFF4CAF50) else Color(0xFFFF9800)
                ) {
                    Text(
                        if (project.isSync) "已同步" else "未同步",
                        fontSize = 10.sp,
                        color = Color.White
                    )
                }
            }

            // 项目详情
            Row(
                modifier = Modifier
                    .fillMaxWidth()
                    .background(Color.White, shape = MaterialTheme.shapes.small)
                    .padding(12.dp),
                horizontalArrangement = Arrangement.SpaceEvenly
            ) {
                Column(horizontalAlignment = Alignment.CenterHorizontally) {
                    Text("大小", fontSize = 11.sp, color = Color.Gray)
                    Text(project.size, fontSize = 13.sp, fontWeight = FontWeight.Bold, color = Color.Black)
                }
                Divider(
                    modifier = Modifier
                        .width(1.dp)
                        .height(30.dp),
                    color = Color(0xFFE0E0E0)
                )
                Column(horizontalAlignment = Alignment.CenterHorizontally) {
                    Text("数据点", fontSize = 11.sp, color = Color.Gray)
                    Text(project.dataCount.toString(), fontSize = 13.sp, fontWeight = FontWeight.Bold, color = Color.Black)
                }
                Divider(
                    modifier = Modifier
                        .width(1.dp)
                        .height(30.dp),
                    color = Color(0xFFE0E0E0)
                )
                Column(horizontalAlignment = Alignment.CenterHorizontally) {
                    Text("最后同步", fontSize = 11.sp, color = Color.Gray)
                    Text(project.lastSync.substringAfter(" "), fontSize = 13.sp, fontWeight = FontWeight.Bold, color = Color.Black)
                }
            }
        }
    }
}

//import androidx.compose.foundation.BorderStroke
//import androidx.compose.material3.Badge
//import androidx.compose.material3.Divider
