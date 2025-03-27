
// 定义更新时间函数
 function updateTitleTime() {
    const now = new Date(); // 获取当前时间
    
    // 提取年、月、日
    const year = now.getFullYear();
    const month = String(now.getMonth() + 1).padStart(2, '0');
    const day = String(now.getDate()).padStart(2, '0');
    
    // 提取时、分、秒并补零
    const hours = String(now.getHours()).padStart(2, '0');
    const minutes = String(now.getMinutes()).padStart(2, '0');
    const seconds = String(now.getSeconds()).padStart(2, '0');
    
    // 组合日期和时间字符串
    const dateString = `${year}-${month}-${day}`;
    const timeString = `${hours}:${minutes}:${seconds}`;
    
    // 更新网页标题和页面头部显示
    // document.title = `当前日期${dateString} 时间${timeString}`;
    const headerTitle = document.querySelector('.header h1');
    if (headerTitle) {
        headerTitle.textContent = `编程竞赛日历 - ${dateString} ${timeString}`;
    }
}

// 页面加载后立即显示时间，并每秒更新一次
window.onload = function() {
    updateTitleTime(); // 立即执行一次
    setInterval(updateTitleTime, 1000); // 每秒更新
};

// 点击事件统计
window.addEventListener('click', function(event) {
    console.log('点击事件:', event.target);
    // 这里可以添加更多的统计逻辑，如发送数据到服务器
});


// 添加过滤函数
function filterData(data, condition) {
    const today = new Date();
    today.setHours(0, 0, 0, 0);
    return data.filter(item => {
        const itemDate = new Date(item.startDate);
        itemDate.setHours(0, 0, 0, 0);
        return itemDate >= today && condition(item);
    });
}