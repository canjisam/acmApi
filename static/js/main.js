// 隐藏菜单
document.addEventListener('click', function() {
  const menu = document.getElementById('custom-menu');
  menu.style.display = 'none';
});

// 新增右键菜单逻辑
const contextMenu = document.getElementById('custom-menu');
document.addEventListener('contextmenu', (e) => {
  e.preventDefault();
  contextMenu.style.display = 'block';
  contextMenu.style.left = `${e.clientX}px`;
  contextMenu.style.top = `${e.clientY}px`;
});

// 整合现有复制功能
function copyToClipboard() {
  const selected = window.getSelection().toString().trim();
  if (selected) {
    const tempElem = document.createElement('textarea');
    tempElem.value = `${selected}\n\n—— Copyright © ${new Date().getFullYear()} canjisam\nSource: https://canjisam.github.io/acmApi/`;
    document.body.appendChild(tempElem);
    tempElem.select();
    document.execCommand('copy');
    document.body.removeChild(tempElem);
  }
}

// 新增分享功能
function sharePage() {
  navigator.share({
    title: document.title,
    url: window.location.href
  }).catch(console.error);
}

// 新增反馈功能
function feedback() {
  window.open('mailto:contact@canjisam.github.io?subject=ACM工具反馈');
}
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
