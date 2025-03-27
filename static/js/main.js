// 自定义右键菜单功能
document.addEventListener('contextmenu', function(e) {
  e.preventDefault();
  
  const menu = document.getElementById('custom-context-menu');
  menu.style.display = 'block';
  menu.style.left = e.pageX + 'px';
  menu.style.top = e.pageY + 'px';
});

// 隐藏菜单
document.addEventListener('click', function() {
  const menu = document.getElementById('custom-context-menu');
  menu.style.display = 'none';
});

// 复制事件处理
document.addEventListener('copy', function(e) {
  const selection = window.getSelection().toString();
  e.clipboardData.setData('text/plain', 
    `${selection}\n\n—— 版权信息 ©${new Date().getFullYear()} canjisam.`
  );
  e.preventDefault();
});