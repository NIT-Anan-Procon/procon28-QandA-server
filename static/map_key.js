/*document.onkeydown = function(e) { 
    var keycode;

    // Mozilla(Firefox, NN) and Opera 
    if (e != null) { 
        keycode = e.which; 
        e.preventDefault(); 
        e.stopPropagation(); 
    } else { 
        keycode = event.keyCode; 
        event.returnValue = false; 
        event.cancelBubble = true; 
    } 

    keychar = String.fromCharCode(keycode).toUpperCase(); 

    if (e.key == "Delete") { 
        alert("Delte");
    } 
    // 特殊キーコードの対応については次を参照 
    // 27   Esc 
    // 8    BackSpace 
    // 9    Tab 
    // 32   Space 
    // 45   Insert 
    // 46   Delete 
    // 35   End 
    // 36   Home 
    // 33   PageUp 
    // 34   PageDown 
    // 38   ↑ 
    // 40   ↓ 
    // 37   ← 
    // 39   → 
    // 処理の例 
    // if (keycode == 27) { 
    //  alert('Escapeキーが押されました'); 
    // } 
} 
*/