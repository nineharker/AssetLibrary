$(document).ready(function() {


	$("#treeview")
	.jstree()
	.on("select_node.jstree", function(e, data){
		var param = "category=" + data.node.text;
		var url = "http://127.0.0.1:8000/upload_form/list/?" + param ;
		location.href=url

    // var xhr= new XMLHttpRequest();
		//
    // xhr.open("GET",url,false);
		// // データをリクエスト ボディに含めて送信する
		// xhr.send();

});


});
