function load(sp) {
    let ke = Object.keys(sp);
    let html = 
            "<form method='POST'>\n" +
            "    <div class='line'>\n" +
            "       <div class='cen' style='margin-left: 37%'>\n" +
            "           <div>\n" +
            "               <a>USER ID</a><a style='margin-left: 120px'>KEY</a>\n" +
            "               <div>\n" +
            "                   <input type='text' name='user'>\n" +
            "                   <input type='text' name='key' id='k'>\n" +
            "               </div>\n" +
            "               <button style='margin-left: 25px;margin-top: 10px' name='key_add' value='key_add'>ADD KEY</button>\n" +
            "               <button style='margin-left: 5px;margin-top: 10px' name='key_del' value='key_del'>DEL KEY</button>\n" +
            "               <button style='margin-left: 5px;margin-top: 10px' onclick='gen_key()'>GENERATE KEY</button>\n" +
            "           </div>\n" +
            "       </div>\n" +
            "   </div>\n" +
            "</form>\n" +
            "<div class='st' style='margin-top:40px'>\n" +
            "    <div class='cen'>\n" +
            "        <table>\n" +
            "            <comment>Key table</comment>\n" +
            "            <tr>\n" +
            "               <th>USER ID</th>\n" +
            "               <th>KEY</th>\n" +
            "               <th>DATE</th>\n";

    for (let i = 0; i < ke.length; i++){
        html += "<tr>\n" +
            "<td>" + ke[i] + "</td>" + "<td>" + sp[ke[i]][0] + "</td>" + "<td>" + sp[ke[i]][1] + "</td>\n" +
            "</tr>";
    }

    html += "            </tr>\n" +
        "        </table>\n" +
        "    </div>\n" +
        "</div>";
    document.getElementById("mesto").innerHTML = html;
}

async function f() {
    const response = await fetch("../static/json/user-key.json")
    .then(res => res.text())
    .then(text => load(JSON.parse(text)))
}

function gen_key(){
    event.preventDefault();
    let str = ''
    arr = ['q', 'w', 'e', 'r', 't', 'y', 'u', 'i', 'o', 'p', 'a', 's', 'd', 'f', 'g', 'h', 'j', 'k', 'l', 'z', 'x', 'c', 'v', 'b', 'n', 'm', 'Q', 'W', 'E', 'R', 'T', 'Y', 'U', 'I', 'O', 'P', 'A', 'S', 'D', 'F', 'G', 'H', 'J', 'K', 'L', 'Z', 'X', 'C', 'V', 'B', 'N', 'M', '1', '2', '3', '4', '5', '6', '7', '8', '9', '0', '$', '%', '&']
    for (let i = 0; i < 41; i++){
        str += arr[Math. floor(Math. random() * arr. length)];
    }
    document.getElementById('k').value = str;
}