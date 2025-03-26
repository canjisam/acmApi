
 // 定义更新时间函数
 function updateTitleTime() {
    const now = new Date(); // 获取当前时间
    
    // 提取时、分、秒并补零
    const hours = String(now.getHours()).padStart(2, '0');
    const minutes = String(now.getMinutes()).padStart(2, '0');
    const seconds = String(now.getSeconds()).padStart(2, '0');
    
    // 组合时间字符串
    const timeString = `${hours}:${minutes}:${seconds}`;
    
    // 更新网页标题
    document.title = `当前时间${timeString}`;
}

// 页面加载后立即显示时间，并每秒更新一次
window.onload = function() {
    updateTitleTime(); // 立即执行一次
    setInterval(updateTitleTime, 1000); // 每秒更新
};