function changeA(x)
    {    
    TableA.deleteRow(x.rowIndex);
    }
    function changeB(x)
    {
   
    TableB.deleteRow(x.rowIndex);
    }
	function enterA()
	{ 
	var first = document.getElementById("itemA").value;
	var last = document.getElementById("priceA").value;

	TableA.innerHTML += '<tr><td><input type = text name = rowA1 value ='+first+'></td>'+'<td><input type = text name = rowA2 rows = 1 cols = 1 value = '+last+'></td><td onclick = changeA(this.parentNode)><button type = button>delete</button></td></tr>';
	
    }
    function enterB()
	{ 
	var first = document.getElementById("itemB").value;
	var last = document.getElementById("priceB").value;
	TableB.innerHTML += '<tr><td><input type = text name = rowB1 value ='+first+'></td>'+'<td><input type = text name = rowB2 rows = 1 cols = 1 value = '+last+'></td><td onclick = changeB(this.parentNode)><button type = button>delete</button></td></tr>';
	
    }