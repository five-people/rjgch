package com.example.xczy.ui.screen

import androidx.compose.foundation.background
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
data class MeasurementRecord(
    val id: Int,
    val projectName: String,
    val date: String,
    val time: String,
    val coordinates: String,
    val deviation: Float,
    val isAbnormal: Boolean = false
)

/**
 * 记录页面 - 查看历史测量记录
 */
@Composable
fun RecordsScreen(modifier: Modifier = Modifier) {
    var selectedFilter by remember { mutableStateOf(0) } // 0: 全部, 1: 异常, 2: 今日

    val recordList = remember {
        listOf(
            MeasurementRecord(
                1,
                "北京中关村项目",
                "2026-04-20",
                "14:30:45",
                "X: 1024.5m, Y: 2048.3m",
                0.05f,
                false
            ),
            MeasurementRecord(
                2,
                "北京中关村项目",
                "2026-04-20",
                "13:45:12",
                "X: 1025.2m, Y: 2047.8m",
                0.12f,
                false
            ),
            MeasurementRecord(
                3,
                "上海浦东工程",
                "2026-04-20",
                "11:20:33",
                "X: 2145.6m, Y: 3456.2m",
                0.48f,
                true
            ),
            MeasurementRecord(
                4,
                "深圳南山施工",
                "2026-04-19",
                "15:15:20",
                "X: 5245.1m, Y: 6234.5m",
                0.08f,
                false
            ),
            MeasurementRecord(
                5,
                "北京中关村项目",
                "2026-04-19",
                "14:10:05",
                "X: 1020.3m, Y: 2050.1m",
                0.65f,
                true
            )
        )
    }

    Column(
        modifier = modifier
            .fillMaxSize()
            .background(Color.White)
    ) {
        // 顶部统计信息
        Card(
            modifier = Modifier
                .fillMaxWidth()
                .padding(16.dp),
            colors = CardDefaults.cardColors(containerColor = Color(0xFFF5F5F5)),
            elevation = CardDefaults.cardElevation(defaultElevation = 2.dp)
        ) {
            Row(
                modifier = Modifier
                    .fillMaxWidth()
                    .padding(16.dp),
                horizontalArrangement = Arrangement.SpaceEvenly
            ) {
                StatisticItem(
                    label = "总记录数",
                    value = recordList.size.toString(),
                    color = Color(0xFF2196F3)
                )
                StatisticItem(
                    label = "异常记录",
                    value = recordList.count { it.isAbnormal }.toString(),
                    color = Color(0xFFFF6B6B)
                )
                StatisticItem(
                    label = "今日记录",
                    value = recordList.count { it.date.endsWith("20") }.toString(),
                    color = Color(0xFF4CAF50)
                )
            }
        }

        // 筛选按钮
        Row(
            modifier = Modifier
                .fillMaxWidth()
                .padding(horizontal = 16.dp)
                .padding(bottom = 12.dp),
            horizontalArrangement = Arrangement.spacedBy(8.dp)
        ) {
            FilterButton(
                label = "全部",
                selected = selectedFilter == 0,
                onClick = { selectedFilter = 0 }
            )
            FilterButton(
                label = "异常",
                selected = selectedFilter == 1,
                onClick = { selectedFilter = 1 }
            )
            FilterButton(
                label = "今日",
                selected = selectedFilter == 2,
                onClick = { selectedFilter = 2 }
            )
        }

        // 记录列表
        LazyColumn(
            modifier = Modifier
                .fillMaxWidth()
                .weight(1f)
                .padding(horizontal = 16.dp),
            verticalArrangement = Arrangement.spacedBy(12.dp)
        ) {
            items(
                recordList.filter { record ->
                    when (selectedFilter) {
                        1 -> record.isAbnormal
                        2 -> record.date.endsWith("20")
                        else -> true
                    }
                }
            ) { record ->
                RecordCard(record)
            }
        }

        // 底部按钮
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
                colors = ButtonDefaults.buttonColors(containerColor = Color(0xFF2196F3)),
                shape = MaterialTheme.shapes.medium
            ) {
                Text("导出数据", fontWeight = FontWeight.Bold)
            }
            Button(
                onClick = { },
                modifier = Modifier
                    .weight(1f)
                    .height(56.dp),
                colors = ButtonDefaults.buttonColors(containerColor = Color(0xFF9C27B0)),
                shape = MaterialTheme.shapes.medium
            ) {
                Text("分析报告", fontWeight = FontWeight.Bold)
            }
        }
    }
}

@Composable
fun StatisticItem(
    label: String,
    value: String,
    color: Color
) {
    Column(
        horizontalAlignment = Alignment.CenterHorizontally,
        verticalArrangement = Arrangement.spacedBy(4.dp)
    ) {
        Text(
            label,
            fontSize = 12.sp,
            color = Color.Gray
        )
        Text(
            value,
            fontSize = 20.sp,
            fontWeight = FontWeight.Bold,
            color = color
        )
    }
}

@Composable
fun FilterButton(
    label: String,
    selected: Boolean,
    onClick: () -> Unit
) {
    OutlinedButton(
        onClick = onClick,
        modifier = Modifier.height(36.dp),
        colors = ButtonDefaults.outlinedButtonColors(
            containerColor = if (selected) Color(0xFF2196F3) else Color.Transparent,
            contentColor = if (selected) Color.White else Color(0xFF2196F3)
        ),
        border = BorderStroke(1.dp, Color(0xFF2196F3)),
        shape = MaterialTheme.shapes.small
    ) {
        Text(label, fontSize = 12.sp)
    }
}

@Composable
fun RecordCard(record: MeasurementRecord) {
    Card(
        modifier = Modifier
            .fillMaxWidth()
            .background(Color.White),
        colors = CardDefaults.cardColors(containerColor = Color.White),
        border = BorderStroke(
            1.dp,
            if (record.isAbnormal) Color(0xFFFF6B6B) else Color(0xFFE0E0E0)
        ),
        elevation = CardDefaults.cardElevation(defaultElevation = 1.dp)
    ) {
        Column(
            modifier = Modifier
                .fillMaxWidth()
                .padding(16.dp),
            verticalArrangement = Arrangement.spacedBy(12.dp)
        ) {
            // 标题行
            Row(
                modifier = Modifier.fillMaxWidth(),
                horizontalArrangement = Arrangement.SpaceBetween,
                verticalAlignment = Alignment.CenterVertically
            ) {
                Column(modifier = Modifier.weight(1f)) {
                    Text(
                        record.projectName,
                        fontSize = 14.sp,
                        fontWeight = FontWeight.SemiBold,
                        color = Color.Black
                    )
                    Text(
                        "${record.date} ${record.time}",
                        fontSize = 12.sp,
                        color = Color.Gray
                    )
                }
                when {
                    record.isAbnormal -> {
                        Badge(
                            containerColor = Color(0xFFFF6B6B)
                        ) {
                            Text("异常", fontSize = 10.sp, color = Color.White)
                        }
                    }
                    record.deviation > 0.2f -> {
                        Badge(
                            containerColor = Color(0xFFFF9800)
                        ) {
                            Text("注意", fontSize = 10.sp, color = Color.White)
                        }
                    }
                    else -> {
                        Badge(
                            containerColor = Color(0xFF4CAF50)
                        ) {
                            Text("正常", fontSize = 10.sp, color = Color.White)
                        }
                    }
                }
            }

            // 坐标信息
            Row(
                modifier = Modifier
                    .fillMaxWidth()
                    .background(Color(0xFFF5F5F5), shape = MaterialTheme.shapes.small)
                    .padding(12.dp)
            ) {
                Text(
                    record.coordinates,
                    fontSize = 12.sp,
                    color = Color(0xFF333333),
                    fontWeight = FontWeight.SemiBold
                )
            }

            // 偏差信息
            Row(
                modifier = Modifier.fillMaxWidth(),
                horizontalArrangement = Arrangement.SpaceBetween,
                verticalAlignment = Alignment.CenterVertically
            ) {
                Text(
                    "偏差值",
                    fontSize = 12.sp,
                    color = Color.Gray
                )
                Text(
                    "%.2f mm".format(record.deviation * 1000),
                    fontSize = 13.sp,
                    fontWeight = FontWeight.Bold,
                    color = if (record.isAbnormal) Color(0xFFFF6B6B) else Color(0xFF2196F3)
                )
            }
        }
    }
}

//import androidx.compose.foundation.BorderStroke
