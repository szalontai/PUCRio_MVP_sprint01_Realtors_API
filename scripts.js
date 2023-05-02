port = ':5050'
window.URL = 'http://127.0.0.1' + port

let IdTipoCorrente = 0

let ImobiliariaCorrente = 0
let ImobiliariaCorrenteByImovel=0
let ImobiliariaSelecionado=0
let QtdeImovelCorrente = 0

let ImovelCorrente = 0
let ImovelCorrenteByComodo = 0
let ImovelSelecionado = 0
let QtdeComodoCorrente

let ComodoCorrente = 0
let ComodoCorrenteByImagem = 0
let ComodoSelecionado = 0
let QtdeImagemCorrente = 0

/*
  ----------------------------------------------------------------------------------------------------
  Função para obter a lista de tipos de imóveis ou de cômodos existente do servidor via requisição GET
  ----------------------------------------------------------------------------------------------------
*/
const Tipo = async (objetos,objeto) => {
  
  // Cria a url
  let url = window.URL + '/'+objetos;

   // Faz a chamada da requisição GET no servidor
  fetch(url, {
    method: 'get',
  })
    .then(async (response) => {

      // Tratamento caso tenha algum erro no retorno do servidor
      if(!response.ok) 
      {
        const text = await response.text()
        throw new Error(JSON.parse(text).mensagem)
      }
      // Retorno o JSON com o itens encontrados no servidor
      return response.json();
    })
    .then(async (data) =>{

        // Monta o objeto data de acordo com o nome do tipo passado
        dataObjeto = eval('data.'+objetos)
        
        if (dataObjeto.length!=0)
          {

             // Cria a lista
            table = document.getElementById(objeto);

            // Apaga todos os itens da lista
            for (var i = 1; i < table.rows.length;) {
              table.deleteRow(i);
            }
          
            // Envio do item adicionado no servidor  para a função que inseri os itens na lista apresentada
            dataObjeto.forEach(item => insertTipoList(item.id, item.descricao,item.qtde,objetos, objeto))
            
            // Mostra a lista
            document.getElementById(objeto).style.display = "block";

            // Mostra o imobiliária
            document.getElementById("fieldsetImobiliaria").style.display = "block";
          }
        else    
        {

          //Esconde a lista
          document.getElementById(objeto).style.display = "none";

          // Esconde o imobiliária
          document.getElementById("fieldsetImobiliaria").style.display = "none";
          
        }      



    })
    .catch((error) => {
      alert(error)
      console.error('Erro:', error);
    });

}

/*
  --------------------------------------------------------------------------------------
  Função para obter a lista de imobiliárias existente do servidor via requisição GET
  --------------------------------------------------------------------------------------
*/
const Imobiliaria = async (objetos,objeto) => {
  
  // Cria a url
  let url = window.URL + '/'+objetos;
  
   // Faz a chamada da requisição GET no servidor
  fetch(url, {
    method: 'get',
  })
    .then(async (response) => {

      // Tratamento caso tenha algum erro no retorno do servidor
      if(!response.ok) 
      {
        const text = await response.text()
        throw new Error(JSON.parse(text).mensagem)
      }
      // Retorno o JSON com o itens encontrados no servidor
      return response.json();
    } )

    .then(async (data) => {
     
        // Monta o objeto data de acordo com o nome do tipo passado
        dataObjeto = eval('data.'+objetos)
        
         if (dataObjeto.length!=0)
         {

          // Cria a lista
          table = document.getElementById(objeto);

           // Apaga todos os itens da lista
          for (var i = 1; i < table.rows.length;) {
            table.deleteRow(i);
          }

          // Envio do item adicionado no servidor  para a função que inseri os itens na lista apresentada        
          dataObjeto.forEach(
            item => insertImobiliariaList(
              item.id,
              item.nome,
              item.razao_social,
              item.cnpj,
              item.ie,
              item.endereco,
              item.complemento,
              item.bairro,
              item.cidade,
              item.uf,
              item.cep,
              item.ddd,
              item.telefone,
              item.matriz,
              item.qtde_filhas,
              item.qtde_filiais,
              objetos,objeto
            ))
             // Mostra a lista da imobiliária
            document.getElementById(objeto).style.display = "block";
            
             // Mostra o imóvel
            document.getElementById("fieldsetImovel").style.display = "block";
            //document.getElementById("formImovel").style.display = "block";

         }
         else
         {

            //Esconde a lista da imobiliária
            document.getElementById(objeto).style.display = "none";

            // Esconde o imóvel
            document.getElementById("fieldsetImovel").style.display = "none";
            //document.getElementById("formImovel").style.display = "none";
         }
    })
    .catch((error) => {
      alert("Atenção. Erro ao incluir. \n" + error);
      //console.error('Error:', error);
    });
}

/*
  --------------------------------------------------------------------------------------
  Função para obter a lista de imoóveis existente do servidor via requisição GET
  --------------------------------------------------------------------------------------
*/
const Imovel = async (objetos,objeto) => {

  // Cria a url
  let url = window.URL + '/'+objetos;
 
   // Faz a chamada da requisição GET no servidor
  fetch(url, {
    method: 'get',
  })
    .then(async (response) => {

      // Tratamento caso tenha algum erro no retorno do servidor
      if(!response.ok) 
      {
        const text = await response.text()
        throw new Error(JSON.parse(text).mensagem)
      }
      // Retorno o JSON com o itens encontrados no servidor
      return response.json();
    } )
   
    .then(async (data) => {

      // Monta o objeto data de acordo com o nome do tipo passado
      dataObjeto = eval('data.'+objetos)
      
      if (dataObjeto.length!=0)
      {

        // Cria a lista
        table = document.getElementById(objeto);

        // Apaga todos os itens da lista
        for (var i = 1; i < table.rows.length;) {
          table.deleteRow(i);
        }
        
        // Envio do item adicionado no servidor  para a função que inseri os itens na lista apresentada
        dataObjeto.forEach(
          item => insertImovelList(
            item.id,
            item.nome,
            item.endereco,
            item.complemento,
            item.bairro,
            item.cidade,
            item.uf,
            item.cep,
            item.ddd,
            item.telefone,
            item.descricao,
            item.imovel,
            item.imobiliaria,
            item.qtde_filhas,
            objeto
        ))
        if (ImobiliariaCorrente==0)
        {
          // Mostra a lista da imóvel
          document.getElementById(objeto).style.display = "none";
        
          // Mostra o formulário do comodo
          document.getElementById("fieldsetComodo").style.display = "none";
        }
        else
        {
          // Mostra a lista da imóvel
          document.getElementById(objeto).style.display = "block";
        
          // Mostra o formulário do comodo
          document.getElementById("fieldsetComodo").style.display = "block";
        }
        //ImovelByImobiliaria(0);
      }
      else
      {
        
        //Esconde a lista do imóvel
        document.getElementById(objeto).style.display = "none";

        // Esconde o comodo
        document.getElementById("fieldsetComodo").style.display = "none";
      }


    })
    .catch((error) => {
      console.error('Error:', error);
    });
}

/*
  --------------------------------------------------------------------------------------
  Função para obter a lista de cômodos existente do servidor via requisição GET
  --------------------------------------------------------------------------------------
*/
const Comodo = async (objetos,objeto) => {

  // Cria a url
  let url = window.URL + '/'+objetos;
 
   // Faz a chamada da requisição GET no servidor
  fetch(url, {
    method: 'get',
  })
    .then(async (response) => {

      // Tratamento caso tenha algum erro no retorno do servidor
      if(!response.ok) 
      {
        const text = await response.text()
        throw new Error(JSON.parse(text).mensagem)
      }
      // Retorno o JSON com o itens encontrados no servidor
      return response.json();
    } )
   
    .then(async (data) => {

      // Monta o objeto data de acordo com o nome do tipo passado
      dataObjeto = eval('data.'+objetos)
      
      if (dataObjeto.length!=0)
      {

        // Cria a lista
        table = document.getElementById(objeto);

        // Apaga todos os itens da lista
        for (var i = 1; i < table.rows.length;) {
          table.deleteRow(i);
        }
        
        // Envio do item adicionado no servidor  para a função que inseri os itens na lista apresentada
        dataObjeto.forEach(
          item => insertComodoList(
            item.id,
            item.imovel,
            item.tipo_comodo,
            item.nome,
            item.quantidade,
            item.descricao,
            item.qtde_filhas,
            objeto
        ))
        // Mostra a lista da comodo
        document.getElementById(objeto).style.display = "none";
      
        // Mostra o formulário da imagem
        document.getElementById("fieldsetImagem").style.display = "none";

        //ImovelByImobiliaria(0);
      }
      else
      {
        
        //Esconde a lista do comodo
        document.getElementById(objeto).style.display = "none";

        // Esconde a imagem
        document.getElementById("fieldsetImagem").style.display = "none";
      }


    })
    .catch((error) => {
      console.error('Error:', error);
    });
}

// Carga do tipo de imóvel
Tipo('tipos_imoveis','tipo_imovel') 

// Carga do tipo de cômodo
Tipo('tipos_comodos','tipo_comodo') 

// Carga da imobiliária
Imobiliaria('imobiliarias','imobiliaria')

// Carga do imovel
Imovel('imoveis','imovel')

// Carga do cômodo
Comodo('comodos','comodo')


// Esconde o formulário da imobiliária
document.getElementById("formImobiliaria").style.display = "none";

// Esconde o formulário e a lista do imóvel
document.getElementById("fieldsetImovel").style.display = "none";
document.getElementById("formImovel").style.display = "none";
document.getElementById("imovel").style.display = "none";

// Esconde o formulário e a lista do cômodo
document.getElementById("fieldsetComodo").style.display = "none";
document.getElementById("formComodo").style.display = "none";
document.getElementById("comodo").style.display = "none";


// Esconde tudo sobre a imagem do cômodo
document.getElementById("fieldsetImagem").style.display = "none";
document.getElementById("formImagem").style.display = "none";
document.getElementById("imagem").style.display = "none";

/*
  --------------------------------------------------------------------------------------
Função para adicionar um novo tipo de imóvel ou cômodo com a descrição
  --------------------------------------------------------------------------------------
*/
const newTipo = (idTIpoDescription,objetos,objeto) => {

  // Captura do campo de descrição
  let inputDescription = document.getElementById(idTIpoDescription).value;

  // Validação da descrição
  if (inputDescription === '') {
    alert("Informe a descrição do tipo !");
  } 
  else 
  {

    // Chama a função que faz a requisição POST
    postTipo(inputDescription,objeto)

    alert("Item adicionado!")

    // Carrega a página novamente
    document.location.reload()
  
  }
}

/*
  -----------------------------------------------------------------------------------------
  Função para colocar um tipo de imóvel ou cômodo na lista do servidor via requisição POST
  -----------------------------------------------------------------------------------------
*/
const postTipo = async (inputDescription, objeto) => {
 
  // Cria o formulário
  const formData = new FormData();

  // Atualiza o formuário com a descrição 
  formData.append('descricao', inputDescription);

  // Cria a url
  let url = window.URL + '/' + objeto;

  // Faz a chamada da requisição POST no servidor
  fetch(url, {
    method: 'post',
    body: formData
  })
    .then( (response) =>response.json() )
    .catch((error) => {
      console.error('Error:', error);
    });

}

/*
  --------------------------------------------------------------------------------------
  Função para inserir itens do tipo de imóvel ou cômodo na lista apresentada
  --------------------------------------------------------------------------------------
*/

const insertTipoList = (id, descricao,qtde,objetos, objeto) => {

  // Criação de array com os itens 
  var item = [id, descricao]

  // Criação da lista
  var table = document.getElementById(objeto);
  
  // Criação das linhas da lista
  var row = table.insertRow();

  // Criação da variavél que indica que o tipo está nas tabelas de imóvel ou cômodo 
  var temFilha = !(qtde == null)

  // Popula as colunas da lista com os itens
  for (var i = 0; i < item.length; i++) {    
    var cel = row.insertCell(i);
    cel.textContent = item[i];
  }
  
  // Monta string com o nome do objeto passado
  objetoName = "close" + objeto

  // Chama a função que cria o botão de excluir item
  insertButton(row.insertCell(-1), objetoName,temFilha)
  
  // Chama a função que cria a função de excluir um item da lista
  removeElement(objetoName,"",objetos,objeto,'Tipo')

}

/*
  --------------------------------------------------------------------------------------
  Função para criar um botão close para cada item da lista
  --------------------------------------------------------------------------------------
*/
const insertButton = (parent, objectName, naomostra) => {

  // Criação do objeto  do tipo span
  let span = document.createElement("span");

  // Criação da caracter x
  let txt = document.createTextNode("\u00D7");
  
  // Associa o nome do objeto ao span
  span.className = objectName;

  // Faz o tratamento para mostrar ou não o objeto de excluir
  if (naomostra) 
  {
    span.style.display = "none"
  }
  else 
  {
    span.style.display = "block"
  }

  // Inclui o carater x no span
  span.appendChild(txt);

  // Inclui o span na coluna da lista
  parent.appendChild(span);
}

/*
  --------------------------------------------------------------------------------------
  Função para remover um item da lista de acordo com o click no botão close
  --------------------------------------------------------------------------------------
*/
const removeElement = (objectName,objectNameCLick,objetos,objeto,ObjetoCarrega) => {

  // Cria o objeto span
  let close = document.getElementsByClassName(objectName);
  
  // Cria o contador
  let i;

  // Faz um loop com todos os objetos de exclusão
  for (i = 0; i < close.length; i++) {

    // Cria a funçao de exclusão
    close[i].onclick = function () 
    {

      // Cria o objeto div
      let div = this.parentElement.parentElement;
      
      // Pega o id do item
      let idItem = div.getElementsByTagName('td')[0].innerHTML
    
      if (confirm("Você tem certeza?")) 
      {
        // Remove div
        div.remove()
      
        // Chama a função de deleta o item de id idItem 
        deleteItem(idItem, objectName)
        alert("Item removido!")

        // Carrega a página novamente
        document.location.reload()
             
      }
    }

  }
}

/*
  --------------------------------------------------------------------------------------
  Função para deletar um item da lista do servidor via requisição DELETE
  --------------------------------------------------------------------------------------
*/
const deleteItem = (id, objectName) => {

  // Monta o nome do objeto para fazer a chamada delete no servidor
  objeto = objectName.substring(5, objectName.length)

  // Cria a url
  let url = window.URL + '/' + objeto + '?id=' + id;

  // Faz a chamada da requisição DELETE no servidor
  fetch(url, {
    method: 'delete'
  })
  .then((response) => response.json())
  .catch((error) => {
    console.error('Error:', error);
  });
  
}

/*
  --------------------------------------------------------------------------------------
  --------------------------------------------------------------------------------------
  
  Funcões para tratamento da imobiliária

  --------------------------------------------------------------------------------------
  --------------------------------------------------------------------------------------
*/

/*
  --------------------------------------------------------------------------------------
  Função para adicionar os campos da imobiliária
  --------------------------------------------------------------------------------------
*/
const newImobiliaria = (objetos,objeto) => {

  // Captura dos campos
  let inputNome = document.getElementById("imobiliariaNewNome").value;
  let inputRazaoSocial = document.getElementById("imobiliariaNewRazaoSocial").value;
  let inputCNPJ = document.getElementById("imobiliariaNewCNPJ").value;
  let inputIE = document.getElementById("imobiliariaNewIE").value;
  let inputEndereco = document.getElementById("imobiliariaNewEndereco").value;
  let inputComplemento = document.getElementById("imobiliariaNewComplemento").value;
  let inputBairro = document.getElementById("imobiliariaNewBairro").value;
  let inputCidade = document.getElementById("imobiliariaNewCidade").value;
  let inputUF = document.getElementById("imobiliariaNewUF").value;
  let inputCEP = document.getElementById("imobiliariaNewCEP").value;
  let inputDDD = document.getElementById("imobiliariaNewDDD").value;
  let inputTelefone = document.getElementById("imobiliariaNewTelefone").value;
  let inputMatriz = document.getElementById("imobiliariaNewMatriz").value;

   // Validação do nome
  if (inputNome === '') {
    alert("Informe o nome da imobiliária !");} 
  else 
    // Validação da razão social 
    if(inputRazaoSocial === '') {
      alert("Informe a razão social da imobiliária !");}
  else
    // Validação do CNPJ 
    if(inputCNPJ === '') {
      alert("Informe o CNPJ da imobiliária !");}
  else 
  {
    
    // Chama a função que faz a requisição POST
    postImobiliaria(
      inputNome,
      inputRazaoSocial,
      inputCNPJ,
      inputIE,
      inputEndereco,
      inputComplemento,
      inputBairro,
      inputCidade,
      inputUF,
      inputCEP,
      inputDDD,
      inputTelefone,
      inputMatriz,
      objeto)

    // Chamo a função que atualiza a lista da imobiliária
    insertImobiliariaList(0,
      inputNome,
      inputRazaoSocial,
      inputCNPJ,
      inputIE,
      inputEndereco,
      inputComplemento,
      inputBairro,
      inputCidade,
      inputUF,
      inputCEP,
      inputDDD,
      inputTelefone,
      inputMatriz,0,0,
      objetos,objeto)
    
    alert("Item adicionado!")

    // Carrega a página novamente
    document.location.reload()

    /*
    // Limpa os campos 
    document.getElementById("imobiliariaNewNome").value="";
    document.getElementById("imobiliariaNewRazaoSocial").value="";
    document.getElementById("imobiliariaNewCNPJ").value="";
    document.getElementById("imobiliariaNewIE").value="";
    document.getElementById("imobiliariaNewEndereco").value="";
    document.getElementById("imobiliariaNewComplemento").value="";
    document.getElementById("imobiliariaNewBairro").value="";
    document.getElementById("imobiliariaNewCidade").value="";
    document.getElementById("imobiliariaNewUF").value="";
    document.getElementById("imobiliariaNewCEP").value="";
    document.getElementById("imobiliariaNewDDD").value="";
    document.getElementById("imobiliariaNewTelefone").value="";
    document.getElementById("imobiliariaNewMatriz").value="";
  
 

      // Cria a lista do objeto
     let table = document.getElementById(objeto);
        
     // Apaga todos os itens da lista
     for (var i = 1; i < table.rows.length;) {
       table.deleteRow(i);
     }
     
     //Escode a lista
     table.style.display = "none";
     
     // Chama a função que fecha o formulário 
     formImobiliaria('C')
     
     // Carrega novamente a lista
     Imobiliaria('imobiliarias','imobiliaria') */

  }
}

/*
  --------------------------------------------------------------------------------------
  Função para colocar um item na lista do servidor via requisição POST
  --------------------------------------------------------------------------------------
*/
const postImobiliaria = async (
  inputNome,
  inputRazaoSocial,
  inputCNPJ,
  inputIE,
  inputEndereco,
  inputComplemento,
  inputBairro,
  inputCidade,
  inputUF,
  inputCEP,
  inputDDD,
  inputTelefone,
  inputMatriz,
  objeto
) => {

  // Cria o formulário
  const formData = new FormData();

  // Atualiza o formulário com os dados da imobiliária
  formData.append('nome', inputNome);
  formData.append('razao_social', inputRazaoSocial);
  formData.append('cnpj', inputCNPJ);
  formData.append('ie', inputIE);
  formData.append('endereco', inputEndereco);
  formData.append('complemento', inputComplemento);
  formData.append('bairro', inputBairro);
  formData.append('cidade', inputCidade);
  formData.append('uf', inputUF);
  formData.append('cep', inputCEP);
  formData.append('ddd', inputDDD);
  formData.append('telefone', inputTelefone);
  formData.append('id_matriz', inputMatriz);

  // Cria a url
  let url = window.URL + '/' + objeto;

  // Faz a chamada da requisição POST no servidor
  fetch(url, {
    method: 'post',
    body: formData
  })
    .then((response) => response.json())
    .catch((error) => {
      console.error('Error:', error);
    }); 

/*   .then(async (response) => {

    // Tratamento caso tenha algum erro no retorno do servidor
    if(!response.ok) 
    {
      const text = await response.text()
      throw new Error(JSON.parse(text).mensagem)
    }

    // Retorno o JSON com o itens encontrados no servidor
    //return response.json()
  })
    .then(async (data) =>{

      alert("Item adicionado !")
      //return response.json()

    })  
    .catch((error) => {
      alert(error)
      console.error('Erro:', error);
    });
 */


}

/*
  --------------------------------------------------------------------------------------
  Função para inserir itens na lista da imobiliária
  --------------------------------------------------------------------------------------
*/
const insertImobiliariaList = (
  id,
  inputNome,
  inputRazaoSocial,
  inputCNPJ,
  inputIE,
  inputEndereco,
  inputComplemento,
  inputBairro,
  inputCidade,
  inputUF,
  inputCEP,
  inputDDD,
  inputTelefone,
  inputMatriz,
  inputQtdeFilhas,
  inputQtdeFiliais,
  objetos, 
  objeto
) => {

   // Criação de array com os itens 
  var item = [id,
    "",
    inputNome,
    inputRazaoSocial,
    inputCNPJ,
    inputIE,
    inputEndereco,
    inputComplemento,
    inputBairro,
    inputCidade,
    inputUF,
    inputCEP,
    inputDDD,
    inputTelefone,
    inputMatriz
  ]

  // Criação da lista
  var table = document.getElementById(objeto);

 
  // Criação das linhas da lista
  var row = table.insertRow();

  // Criação da variavél que indica que o imobiliária tem algum imóvel 
  var temImovel = !(inputQtdeFilhas == null)

  // Popula as colunas da lista com os itens
  for (var i = 0; i < item.length; i++) {

    var cel = row.insertCell(i);

    if (i == 1) {
    
      // Cria um checkbox na segunda coluna da lista
      let chk = document.createElement("INPUT");
      chk.setAttribute("type", "checkbox");
      chk.className = "selectimobiliaria";
      chk.id = "idselectimobiliaria";

      if (temImovel) 
      {
        // Se a imobiliária tiver um imóvel, o checkbox aparece 
        chk.style.display = "block"
        
        // Se a imobiliária tiver sido clicada antes, ela aparecerá como marcada
        if (ImobiliariaCorrente==id) 
        {
          chk.checked = true
          if (document.getElementById("idselectimobiliaria")!=null) 
            document.getElementById("idselectimobiliaria").onclick()
        } 

      }
      else {
        // Se a imobiliária não tiver um imóvel, o checkbox não aparece 
        chk.style.display = "none"
      }
      cel.appendChild(chk);
    }

    else
      cel.textContent = item[i];
  }

  // Se a imobiliária não tiver um imóvel, mas tiver uma filial, 
  // força o variável temImovel como true para não aparecer o X de 
  // apagar o item
  if (!temImovel && inputQtdeFiliais!=null)
    temImovel = true
  
    
  // Chama a função que cria o botão de excluir item
  insertButton(row.insertCell(-1), "closeimobiliaria", temImovel)

  // Chama a função que cria a função de excluir um item da lista
  removeElement("closeimobiliaria","",objetos, objeto,'Imobiliaria')
  
  // Chama a função que cria a função de selecionar os itens filhos da imobiliária
  selectImobiliaria()
  //selectImovel()

  if ( temImovel && (ImobiliariaCorrente==id) )
    document.getElementById("idselectimobiliaria").onclick()

}

/*
  --------------------------------------------------------------------------------------
  Função para criar a função de selecionar os itens filhos da imobiliária
  --------------------------------------------------------------------------------------
*/
const selectImobiliaria = () => {

  // Cria o objeto select
  let select = document.getElementsByClassName("selectimobiliaria");

  // Cria o contador
  let i;
  
  // Faz um loop com todos os objetos de seleção
  for (i = 0; i < select.length; i++) {

    // Cria a funçao de seleção
    select[i].onclick = function () 
    {     
      // Cria o objeto div
      let div = this.parentElement.parentElement;
      
      // Pega o id do item
      const idItem = div.getElementsByTagName('td')[0].innerHTML

       // Cria o evento de click
      div.addEventListener('click', (event) => {

        // Faz uma pesquisa para trazer todos o checkbox que estão selecionados
        let checkboxes = document.querySelectorAll('input[class="selectimobiliaria"]:checked');

        //let values = [];

        // faz um lop com os checkbox selecionados
        checkboxes.forEach((checkbox) => 
        {
          // Pega o id do checkbox selecionado
          let curChk = checkbox.parentElement.parentElement.innerHTML[4];

          if (curChk != idItem) {

            // Caso o id do checkbox selecionado for diferente do atual, eu desmarco ele
            checkbox.checked = false
            return false;
          }
          //else{
           // div.style.background = "rgb(91, 152, 209)"
          //}
          //values.push(checkbox.value);
        }
        );
        //alert(values);
      });

      if (this.checked || ImobiliariaCorrenteByImovel!=0)
      {
        // Se o item atual estiver marcado, 
        // chama a função que carrega o imóvel
        if (ImobiliariaCorrenteByImovel!=0)
          ImovelByImobiliaria(ImobiliariaCorrenteByImovel);
        else
          ImovelByImobiliaria(idItem);
      }
      else 
      {
        // Limpa a lista do imóvel
        let table = document.getElementById("imovel");
        table.style.display = "none";

        ImovelByImobiliaria(0);
      
      }

    }

  }
}

/*
  --------------------------------------------------------------------------------------
  Função para abrir ou fechar o formulário da imobiliária e montar ou zerar o 
  DropdownList das imobiliárias
  --------------------------------------------------------------------------------------
*/
const formImobiliaria = (tipo) => {

  // Se a opção for 'O' abre o formulário
  if (tipo=='O')
    document.getElementById("formImobiliaria").style.display = "block"
  else
    document.getElementById("formImobiliaria").style.display = "none"

  // Chama a função que monta o DropdownList com a relação das imobiliárias

  dynamicDropdownList(tipo,'imobiliarias','imobiliariaNewMatriz','imobiliariaNewMatrizId')
  
}

/*
  --------------------------------------------------------------------------------------
  Função para obter a lista existente do servidor via requisição GET
  --------------------------------------------------------------------------------------
*/
const ImovelByImobiliaria = async (id_imobiliaria,objetos,objeto) => {

  let url = window.URL + '/imoveisByImobiliaria?id_imobiliaria=' + id_imobiliaria;
  var table = document.getElementById("imovel");
  ImobiliariaCorrente = id_imobiliaria

  console.log("ImobiliariaCorrente = "+ImobiliariaCorrente)

  // Limpando a lista dos imóveis
  for (var i = 1; i < table.rows.length;) {
    table.deleteRow(i);
  }

   // Escondendo o formulário do cômodo
  table = document.getElementById("fieldsetComodo");
  table.style.display = "none";
  
  // Limpando e escondendo a lista dos cômodos
  table = document.getElementById("comodo");
  for (var i = 1; i < table.rows.length;) {
    table.deleteRow(i);
  }
  table.style.display = "none";
  
   // Escondendo o formulário da imagem
  table = document.getElementById("fieldsetImagem");
  table.style.display = "none";

  // Limpando e escondendo a lista das imagens
  table = document.getElementById("imagem");
  for (var i = 1; i < table.rows.length;) {
    table.deleteRow(i);
  }
  table.style.display = "none";
  
  // Voltando para a lista dos imóveis
  table = document.getElementById("imovel");

  if (id_imobiliaria != 0) {

    // Mostrando a lista do imóvel
    table.style.display = "block";

    // Mostrando o formulário da cômodo
    document.getElementById("fieldsetComodo").style.display = "block";
  
    //document.getElementById("fieldsetImovel").style.display = "block"
    fetch(url, { method: 'get', })
      .then( async (response) => {
      
        // Retorno o JSON com o itens encontrados no servidor
      return response.json();
    })
      .then( async (data) => {
        data.imoveis.forEach(
          item => insertImovelList(
            item.id,
            item.nome,
            item.endereco,
            item.complemento,
            item.bairro,
            item.cidade,
            item.uf,
            item.cep,
            item.ddd,
            item.telefone,
            item.descricao,
            item.imovel,
            item.imobiliaria,
            item.qtde_filhas,
            'imovel'
          ))
      })
      .catch((error) => {
        console.error('Error:', error);
      }); 
    
/*     // Cria a lista do objeto
    table = document.getElementById('imovel');
        
    // Apaga todos os itens da lista
    for (var i = 1; i < table.rows.length;) {
      table.deleteRow(i);
    }
     */
    //Escode a lista
    table.style.display = "none";
         
      // Carga do imovel
    //Imovel('imoveis','imovel')

    // Mostra a lista da imóvel
    document.getElementById('imovel').style.display = "block";

    // Mostra o formulário do comodo
    document.getElementById("fieldsetComodo").style.display = "block";
  }
}

/*
  --------------------------------------------------------------------------------------
  --------------------------------------------------------------------------------------
  
  Funcões para tratamento do imóvel

  --------------------------------------------------------------------------------------
  --------------------------------------------------------------------------------------
*/

/*
  --------------------------------------------------------------------------------------
  Função para adicionar os campos do imóvel
  --------------------------------------------------------------------------------------
*/
const newImovel = (objetos,objeto) => {
  
  // Captura dos campos
  let inputNome = document.getElementById("imovelNewNome").value;
  let inputEndereco = document.getElementById("imovelNewEndereco").value;
  let inputComplemento = document.getElementById("imovelNewComplemento").value;
  let inputBairro = document.getElementById("imovelNewBairro").value;
  let inputCidade = document.getElementById("imovelNewCidade").value;
  let inputUF = document.getElementById("imovelNewUF").value;
  let inputCEP = document.getElementById("imovelNewCEP").value;
  let inputDDD = document.getElementById("imovelNewDDD").value;
  let inputTelefone = document.getElementById("imovelNewTelefone").value;
  let inputDescricao = document.getElementById("imovelNewDescricao").value;
  let inputTipoImovel = document.getElementById("imovelNewTipoImovelId").value;
  let inputImobiliaria = document.getElementById("imovelNewImobiliariaId").value;

  // Validação da imobiliária
  if (inputImobiliaria === undefined) {
    alert("Informe a imobiliária!");
  } 
  else
    // Validação do nome
    if (inputNome === '') {
      alert("Informe o nome do imóvel!");
    } 
  else
    // Validação do tipo do imóvel
    if (inputTipoImovel === undefined) {
      alert("Informe o tipo de imóvel!");
    } 
  else 
  {
    // Tratamento do DDD
    if(inputDDD ==="")
    {
      inputDDD = '11'
    }
    
    // Chama a função que faz a requisição POST
    postImovel(
      inputNome,
      inputEndereco,
      inputComplemento,
      inputBairro,
      inputCidade,
      inputUF,
      inputCEP,
      inputDDD,
      inputTelefone,
      inputDescricao,
      inputTipoImovel,
      inputImobiliaria,
      objeto)
   
    // Chamo a função que atualiza a lista do imóvel
    insertImovelList(0,
      inputNome,
      inputEndereco,
      inputComplemento,
      inputBairro,
      inputCidade,
      inputUF,
      inputCEP,
      inputDDD,
      inputTelefone,
      inputDescricao,
      inputTipoImovel,
      inputImobiliaria,0,
      objeto)
    
    alert("Item adicionado!")

    // Carrega a página novamente
    document.location.reload()
/*
    // Limpa os campos do formulário
    document.getElementById("imovelNewNome").value=""
    document.getElementById("imovelNewEndereco").value=""
    document.getElementById("imovelNewComplemento").value=""
    document.getElementById("imovelNewBairro").value=""
    document.getElementById("imovelNewCidade").value=""
    document.getElementById("imovelNewUF").value=""
    document.getElementById("imovelNewCEP").value=""
    document.getElementById("imovelNewDDD").value=""
    document.getElementById("imovelNewTelefone").value=""
    document.getElementById("imovelNewDescricao").value=""
    document.getElementById("imovelNewTipoImovelId").value=""
    document.getElementById("imovelNewImobiliariaId").value=""

     // Fecha o formulário 
     formImovel('C')

  // Tratamento para montar as listas carregadas após a inclusão
  if (QtdeImovelCorrente==0)
  {
    ImobiliariaCorrenteByImovel = ImobiliariaCorrente
    document.getElementById("idselectimobiliaria").onclick()
  }
  else
  {
    if (ImobiliariaSelecionado!=ImobiliariaCorrente){
      //document.getElementById("idselectimovel").onclick()

      if (ImobiliariaCorrente!=0)
      {
        ImobiliariaCorrenteByImovel = ImobiliariaSelecionado
        document.getElementById("idselectimobiliaria").onclick()
      }      
      else
        document.getElementById("idselectimobiliaria").onclick()
      
    }
    else{        
      if (ImobiliariaCorrente!=0)
      {
        ImobiliariaCorrenteByImovel = ImobiliariaCorrente
        document.getElementById("idselectimobiliaria").onclick()
      }      
      else
        document.getElementById("idselectimobiliaria").onclick()
    }
  }
 */
  ImobiliariaCorrenteByImovel = 0
  QtdeImovelCorrente = 0

 
/*
    // Cria a lista do objeto
    let table = document.getElementById(objeto);
        
    // Apaga todos os itens da lista
    for (var i = 1; i < table.rows.length;) {
      table.deleteRow(i);
    }
    
    //Escode a lista
    table.style.display = "none";
    
    // Chama a função que fecha o formulário 
    formImovel('C')

  // Carga do tipo de imóvel
  Tipo('tipos_imoveis','tipo_imovel') 
    
  // Carrega novamente a lista
  Imobiliaria('imobiliarias','imobiliaria')
 */


 /*    // limpa a lista da imobiliaria
    table = document.getElementById("imobiliaria");
    
    // Limpando a lista dos imóveis
    for (var i = 1; i < table.rows.length;) {
      table.deleteRow(i);
    }
 */
  
  }
}

/*
    --------------------------------------------------------------------------------------
  Função para colocar um item na lista do servidor via requisição POST
  --------------------------------------------------------------------------------------
*/
const postImovel = async (
  inputNome,
  inputEndereco,
  inputComplemento,
  inputBairro,
  inputCidade,
  inputUF,
  inputCEP,
  inputDDD,
  inputTelefone,
  inputDescricao,
  inputTipoImovel,
  inputImobiliaria,
  objeto
) => {

   // Cria o formulário
  const formData = new FormData();

  // Atualiza o formulário com os dados do imóvel
  formData.append('nome', inputNome);
  formData.append('endereco', inputEndereco);
  formData.append('complemento', inputComplemento);
  formData.append('bairro', inputBairro);
  formData.append('cidade', inputCidade);
  formData.append('uf', inputUF);
  formData.append('cep', inputCEP);
  formData.append('ddd', inputDDD);
  formData.append('telefone', inputTelefone);
  formData.append('descricao', inputDescricao);
  formData.append('id_tipo_imovel', inputTipoImovel);
  formData.append('id_imobiliaria', inputImobiliaria);

  // Cria a url
  let url = window.URL + '/' + objeto;

  // Faz a chamada da requisição POST no servidor
  fetch(url, {
    method: 'post',
    body: formData
  })
    .then((response) => response.json())
    .catch((error) => {
      console.error('Error:', error);
    });
 
  /*
  .then(async response => 
    {
    if(!response.ok) {
      const text = await response.text()
      throw new Error(text)
     }
    else {
      alert("Item adicionado !")
   }    
    })
    .catch((error) => {

      alert(error);
      console.error('Error:', error);
    });
*/

}
/*
  --------------------------------------------------------------------------------------
  Função para inserir itens na lista apresentada
  --------------------------------------------------------------------------------------
*/

const insertImovelList = (
  id,
  inputNome,
  inputEndereco,
  inputComplemento,
  inputBairro,
  inputCidade,
  inputUF,
  inputCEP,
  inputDDD,
  inputTelefone,
  inputDescricao,
  inputTipoImovel,
  inputImobiliaria,
  inputQtdeFilhas,
  objeto) => {

   // Criação de array com os itens    
  var item = [id,
    "",
    inputImobiliaria,
    inputNome,
    inputEndereco,
    inputComplemento,
    inputBairro,
    inputCidade,
    inputUF,
    inputCEP,
    inputDDD,
    inputTelefone,
    inputDescricao,
    inputTipoImovel
  ]
  // Criação da lista
  var table = document.getElementById(objeto);

  // Criação das linhas da lista
  var row = table.insertRow();

  // Criação da variavél que indica que o imoóvel tem algum cômodo 
  var temComodo = !(inputQtdeFilhas == null)

  // Popula as colunas da lista com os itens
  for (var i = 0; i < item.length; i++) {

    var cel = row.insertCell(i);
    
    if (i == 1) {

      // Cria um checkbox na segunda coluna da lista
      let chk = document.createElement("INPUT");
      chk.setAttribute("type", "checkbox");
      chk.className = "selectimovel";
      chk.id = "idselectimovel";
      
      if (temComodo) {
      
        // Se a imobiliária tiver um imóvel, o checkbox aparece 
        chk.style.display = "block"
      }
      else 
      {  
        // Se a imobiliária não tiver um imóvel, o checkbox não aparece 
        chk.style.display = "none"
      }
      cel.appendChild(chk);
    }
    else
      cel.textContent = item[i];
  }

  // Chama a função que cria o botão de excluir item
  insertButton(row.insertCell(-1), "closeimovel", temComodo)
 
  // Chama a função que cria a função de excluir um item da lista
  removeImovel("closeimovel")
 
  // Chama a função que cria a função de selecionar os itens filhos da imóvel
  selectImovel()

  //if ( temComodo && (ImovelCorrente==id) )
  //document.getElementById("idselectimovel").onclick()

}

/*
  --------------------------------------------------------------------------------------
  Função para remover um item da lista de acordo com o click no botão close
  --------------------------------------------------------------------------------------
*/
const removeImovel = (objectName) => {

  // Cria o objeto span
  let close = document.getElementsByClassName(objectName);
  
  // Cria o contador
  let i;

  // Faz um loop com todos os objetos de exclusão
  for (i = 0; i < close.length; i++) {

    // Cria a funçao de exclusão
    close[i].onclick = function () 
    {

      // Cria o objeto div
      let div = this.parentElement.parentElement;
      
      // Pega o id do item
      let idItem = div.getElementsByTagName('td')[0].innerHTML
    
      if (confirm("Você tem certeza?")) 
      {
        // Remove div
        div.remove()
      
        // Chama a função de deleta o item de id idItem 
        deleteItem(idItem, objectName)
       alert("Item removido!")

        // Carrega a página novamente
        document.location.reload()
/*      

        // Carga do tipo de imóvel
        Tipo('tipos_imoveis','tipo_imovel') 

        // Carga da imobiliária
        Imobiliaria('imobiliarias','imobiliaria')

        // Carga do imovel
        Imovel('imoveis','imovel') */

        // Tratamento para montar as listas carregadas após a exclusão
/*         if (QtdeImovelCorrente>1)
        {
          ImobiliariaCorrenteByImovel = ImobiliariaCorrente
          document.getElementById("idselectimobiliaria").onclick()
        }
        else
          document.getElementById("idselectimobiliaria").onclick()
         */
        ImobiliariaCorrenteByImovel = 0
        QtdeImovelCorrente=0
       
      }
    }

  }
}

/*
  --------------------------------------------------------------------------------------
   Função para criar a função de selecionar os itens filhos do imóvel
  --------------------------------------------------------------------------------------
*/
const selectImovel = () => {

  // Cria o objeto select
  let select = document.getElementsByClassName("selectimovel");
  
  // Cria o contador
  let i;

  // Faz um loop com todos os objetos de seleção
  for (i = 0; i < select.length; i++) {

    // Cria a função de seleção
    select[i].onclick = function () 
    {
      // Cria o objeto div
      let div = this.parentElement.parentElement;

      // Pega o id do item
      const idItem = div.getElementsByTagName('td')[0].innerHTML

      // Cria o evento de click
      div.addEventListener('click', (event) => {
        
        // Faz uma pesquisa para trazer todos o checkbox que estão selecionados
        let checkboxes = document.querySelectorAll('input[className="selectimovel"]:checked');

        // faz um lop com os checkbox selecionados
        checkboxes.forEach((checkbox) => 
        {
          // Pega o id do checkbox selecionado
          let curChk = checkbox.parentElement.parentElement.innerHTML[4];
          
          if (curChk != idItem) {

            // Caso o id do checkbox selecionado for diferente do atual, eu desmarco ele
            checkbox.checked = false
            return false;
          }
          //values.push(checkbox.value);
        }
        );
        //alert(values);
      });

      if (this.checked ||  ImovelCorrenteByComodo!=0 )
      {
        // Se o item atual estiver marcado, 
        // chama a função que carrega o cômodo
        if (ImovelCorrenteByComodo!=0)
          ComodoByImovel(ImovelCorrenteByComodo);
        else
          ComodoByImovel(idItem);
      }
      else 
      {
        // Limpa a lista do cômodo
        let table = document.getElementById("comodo");

        table.style.display = "none";
        for (var i = 1; i < table.rows.length;) {
          table.deleteRow(i);
        }

        // Limpa a lista da imagem do cômodo
        table = document.getElementById("fieldsetImagem");
        table.style.display = "none";

        table = document.getElementById("imagem");
        for (var i = 1; i < table.rows.length;) {
          table.deleteRow(i);
        }
        
        ComodoByImovel(0);
      }

    }

  }
}

/*
  --------------------------------------------------------------------------------------
  Função para abrir ou fechar o formulário do imóvel e montar ou zerar o DropdownList 
  das imobiliárias e os tipos de imóveis
  --------------------------------------------------------------------------------------
*/
const formImovel = (tipo) => {

    // Se a opção for 'O' abre o formulário
  if (tipo=='O')
    document.getElementById("formImovel").style.display = "block"
  else
    document.getElementById("formImovel").style.display = "none"

  
  // Chama a função que monta o DropdownList com a relação das imobiliárias para os imóveis
  dynamicDropdownList(tipo,'imobiliarias','imovelNewImobiliaria','imovelNewImobiliariaId')

  // Chama a função que monta o DropdownList com a relação das tipo de imóveis
  dynamicDropdownListTipoImovel(tipo)
  
}

/*
  --------------------------------------------------------------------------------------
  Função para obter a lista existente do servidor via requisição GET
  --------------------------------------------------------------------------------------
*/
const ComodoByImovel = async (id_imovel) => {

  let url = window.URL + '/comodosByImovel?id_imovel=' + id_imovel;
  var table = document.getElementById("comodo");
  ImovelCorrente = id_imovel
  //ImovelSelecionado = id_imovel
  console.log("ImovelCorrente = "+ImovelCorrente)
  
  // Limpando a lista dos cômodos
  for (var i = 1; i < table.rows.length;) {
    table.deleteRow(i);
  }

  // Escondendo o formulário da imagem
  table = document.getElementById("fieldsetImagem");
  table.style.display = "none";

   // Limpando a lista das imagens
  table = document.getElementById("imagem");
  for (var i = 1; i < table.rows.length;) {
    table.deleteRow(i);
  }
  
  // Escondendo lista da imagem
  table.style.display = "none";
  
  // Voltando para a lista dos cômodos
  table = document.getElementById("comodo");
  
  if (id_imovel != 0) {
    
    // Mostrando a lista do cômodo
    table.style.display = "block";

    // Mostrando o formulário da imagem
    document.getElementById("fieldsetImagem").style.display = "block";
    
    fetch(url, {
      method: 'get',
    })
      .then((response) => response.json())
      .then((data) => {

        QtdeComodoCorrente = data.comodos.length

        data.comodos.forEach(
          item => insertComodoList(
            item.id,
            item.imovel,
            item.tipo_comodo,
            item.nome,
            item.quantidade,
            item.descricao,
            item.qtde_filhas,
            'comodo'
          ))
      })
      .catch((error) => {
        console.error('Error:', error);
      });
  }
}

/*
  --------------------------------------------------------------------------------------
  Função que monta o DropdownList genérica com a relação de itens
  --------------------------------------------------------------------------------------
*/
const dynamicDropdownList = async (tipo,tabela,objeto,objetoId) => {

  // Captura dos campos
  var selectObjeto = document.getElementById(objeto);
  var selectObjetoId = document.getElementById(objetoId);

  if (tipo=="O") // Opção para carregar a lista
  {
     // Cria a url
    let url = window.URL + '/'+tabela;

    // Faz a chamada da requisição POST no servidor
    fetch(url, {
      method: 'get',
    })
      .then((response) => response.json())
      .then((data) => {

        tipos = eval("data."+tabela)

        // Monta a primeira linha em branco
        let option = document.createElement("option");
        let optionText = document.createTextNode("");

        option.setAttribute('value', "0");
        option.appendChild(optionText);
        selectObjeto.appendChild(option);

         // Popula as demais linhas
        for (var i = 0; i < tipos.length; i++) {

          let option = document.createElement("option");
          let optionText = document.createTextNode(tipos[i].nome);

          option.setAttribute('value', tipos[i].id);
          option.appendChild(optionText);
          selectObjeto.appendChild(option);
        }

        // Cria o evento de selecionar o item
        selectObjeto.addEventListener("change", e => {
          selectObjetoId.value = e.target.value;
        })

      })
      .catch((error) => {
        console.error('Error:', error);
      });
    }
    else{
      // Opção para limpar a lista
      while (selectObjeto.hasChildNodes()) {
        selectObjeto.removeChild(selectObjeto.firstChild);
      }
    }
}

/*
  --------------------------------------------------------------------------------------
  Função que monta o DropdownList com a relação das imóveis para os comôdos
  --------------------------------------------------------------------------------------
*/
const dynamicDropdownListImovel = async (tipo) => {

  // Captura dos campos
  var comodoNewImovel = document.getElementById("comodoNewImovel");
  var comodoNewImovelId = document.getElementById("comodoNewImovelId");

  if (tipo=="O") // Opção para carregar a lista
  {
    // Cria a url
    let url = window.URL + '/imoveisByImobiliaria?id_imobiliaria=' + ImobiliariaCorrente;

    // Faz a chamada da requisição POST no servidor
    fetch(url, {
      method: 'get',
    })
      .then((response) => response.json())
      .then((data) => {

        tipos = data.imoveis

        // Monta a primeira linha em branco
        let option = document.createElement("option");
        let optionText = document.createTextNode("");

        option.setAttribute('value', 0);
        option.appendChild(optionText);
        comodoNewImovel.appendChild(option);

        // Popula as demais linhas
        for (var i = 0; i < tipos.length; i++) {

          let option = document.createElement("option");
          let optionText = document.createTextNode(tipos[i].nome);

          option.setAttribute('value', tipos[i].id);
          option.appendChild(optionText);
          comodoNewImovel.appendChild(option);
        }

        // Cria o evento de selecionar o item
        comodoNewImovel.addEventListener("change", e => {
          comodoNewImovelId.value = e.target.value;
        })

      })
      .catch((error) => {
        console.error('Error:', error);
      });
    }
    else{
      // Opção para limpar a lista
      while (comodoNewImovel.hasChildNodes()) {
        comodoNewImovel.removeChild(comodoNewImovel.firstChild);
      }
    }
}

/*
  --------------------------------------------------------------------------------------
  Função  que monta o DropdownList com a relação das tipo de imóveis
  --------------------------------------------------------------------------------------
*/
const dynamicDropdownListTipoImovel = async (tipo) => {

  // Captura dos campos
  const imovelNewTipoImovel = document.getElementById("imovelNewTipoImovel");
  const imovelNewTipoImovelId = document.getElementById("imovelNewTipoImovelId");

  if (tipo=="O")// Opção para carregar a lista
  {
    // Cria a url
    let url = window.URL + '/tipos_imoveis';

    // Faz a chamada da requisição POST no servidor
    fetch(url, {
      method: 'get',
    })
      .then((response) => response.json())
      .then((data) => {

        tipos = data.tipos_imoveis

        // Monta a primeira linha em branco
        let option = document.createElement("option");
        let optionText = document.createTextNode("");

        option.setAttribute('value', 0);
        option.appendChild(optionText);
        imovelNewTipoImovel.appendChild(option);

        // Popula as demais linhas
        for (var i = 0; i < tipos.length; i++) {

          let option = document.createElement("option");
          let optionText = document.createTextNode(tipos[i].descricao);

          option.setAttribute('value', tipos[i].id);
          option.appendChild(optionText);
          imovelNewTipoImovel.appendChild(option);

        }

        // Cria o evento de selecionar o item  
        imovelNewTipoImovel.addEventListener("change", e => {
          imovelNewTipoImovelId.value = e.target.value;
        })


      })
      .catch((error) => {
        console.error('Error:', error);
      });
    }
    else{
      // Opção para limpar a lista
      while (imovelNewTipoImovel.hasChildNodes()) {
        imovelNewTipoImovel.removeChild(imovelNewTipoImovel.firstChild);
      }
    }
}

/*
  --------------------------------------------------------------------------------------
  --------------------------------------------------------------------------------------
  
  Funcões para tratamento do comôdo

  --------------------------------------------------------------------------------------
  --------------------------------------------------------------------------------------
*/

/*
  --------------------------------------------------------------------------------------
  Função para adicionar os campos do cômodo
  --------------------------------------------------------------------------------------
*/
const newComodo = (objetos,objeto) => {

  // Captura dos campos
  let inputImovel = document.getElementById("comodoNewImovel").value;
  let inputTipoComodo = document.getElementById("comodoNewTipoComodo").value;
  let inputNome = document.getElementById("comodoNewNome").value;
  let inputQuantidade = document.getElementById("comodoNewQuantidade").value;
  let inputDescricao = document.getElementById("comodoNewDescricao").value;

   // Validação do imóvel
  if (inputImovel === '0') {
    alert("Informe o imóvel!");
  } 
  else
    // Validação do tipo do cômodo 
    if (inputTipoComodo === '0') {
      alert("Informe o tipo de cômodo!");
    } 
  else
    // Validação do nome
    if (inputNome === '') {
      alert("Informe o nome do cômodo!");
    } 
  else 
    // Validação da qtde
    if (inputQuantidade === '0' || inputQuantidade === '') {
      alert("Informe a quantidade do cômodo!");
    } 
  else 
  {
    // Chama a função que faz a requisição POST
    postComodo(
      inputImovel,
      inputTipoComodo,
      inputNome,
      inputQuantidade,
      inputDescricao,
      objeto
    )
  
    alert("Item adicionado!")

    // Limpa os campos do formulário
    document.getElementById("comodoNewImovel").value=""
    document.getElementById("comodoNewTipoComodo").value=""
    document.getElementById("comodoNewNome").value=""
    document.getElementById("comodoNewQuantidade").value=""
    document.getElementById("comodoNewDescricao").value=""
  
    // Fecha o formulário
    formComodo('C')

    // Tratamento para montar as listas carregadas após a inclusão
    if (QtdeComodoCorrente==0)
    {
      ImobiliariaCorrenteByImovel = ImobiliariaCorrente
      document.getElementById("idselectimobiliaria").onclick()
    }
    else
    {
      if (ImovelSelecionado!=ImovelCorrente){
        //document.getElementById("idselectimovel").onclick()

        if (ImovelCorrente!=0)
        {
          ImovelCorrenteByComodo = ImovelSelecionado
          document.getElementById("idselectimovel").onclick()
        }      
        else
          document.getElementById("idselectimobiliaria").onclick()
        
      }
      else{        
        if (ImovelCorrente!=0)
        {
          ImovelCorrenteByComodo = ImovelCorrente
          document.getElementById("idselectimovel").onclick()
        }      
        else
          document.getElementById("idselectimobiliaria").onclick()
      }
    }
    ImovelCorrenteByComodo = 0
    QtdeComodoCorrente =0

    // Carga do tipo de cômodo
    Tipo('tipos_comodos','tipo_comodo') 

/*     // Limpa os campos 
    document.getElementById("comodoNewNome").value=""
    document.getElementById("comodoNewQuantidade").value=""
    document.getElementById("comodoNewDescricao").value = ""
  
    // Cria a lista do objeto
    let table = document.getElementById(objeto);
      
    // Apaga todos os itens da lista
    for (var i = 1; i < table.rows.length;) {
      table.deleteRow(i);
    }
    
    //Escode a lista
    table.style.display = "none";
  
    // Chama a função que fecha o formulário 
    formComodo('C')

    // ??
    document.getElementById("idselectimobiliaria").onclick()

    // Carga do tipo de cômodo
    Tipo('tipos_comodos','tipo_comodo') 

    // Carrega novamente a lista
    Imovel('imoveis','imovel')
  */

  }
}

/*
  --------------------------------------------------------------------------------------
  Função para colocar um item na lista do servidor via requisição POST
  --------------------------------------------------------------------------------------
*/
const postComodo = async (
  inputImovel,
  inputTipoComodo,
  inputNome,
  inputQuantidade,
  inputDescricao,
  objeto
) => {

   // Cria o formulário
  const formData = new FormData();

  ImovelSelecionado = inputImovel
  // Atualiza o formulário com os dados do cômodo
  formData.append('id_imovel', inputImovel);
  formData.append('id_tipo_comodo', inputTipoComodo);
  formData.append('nome', inputNome);
  formData.append('quantidade', inputQuantidade);
  formData.append('descricao', inputDescricao);

  // Cria a url
  let url = window.URL + '/' + objeto;

  // Faz a chamada da requisição POST no servidor
  fetch(url, {
    method: 'post',
    body: formData
  })
    .then((response) => response.json())
/*     .then((data) =>{

/*       // Chamo a função que atualiza a lista do cômodo
      insertComodoList(
        data.id,
        data.imovel,
        data.tipo_comodo,
        data.nome,
        data.quantidade,
        data.descricao,
        data.qtde_filhas,
        objeto
      ) 
    }) */
    .catch((error) => {
      console.error('Error:', error);
    });
}

/*
  --------------------------------------------------------------------------------------
  Função para inserir itens na lista apresentada
  --------------------------------------------------------------------------------------
*/

const insertComodoList = (
  id,
  inputImovel,
  inputTipoComodo,
  inputNome,
  inputQuantidade,
  inputDescricao,
  inputQtdeFilha,
  objeto
) => {

  // Criação de array com os iten
  var item = [
    id,
    "",
    inputImovel,
    inputNome,
    inputQuantidade,
    inputDescricao,
    inputTipoComodo
  ]
  // Criação da lista
  var table = document.getElementById(objeto);

  // Criação das linhas da lista
  var row = table.insertRow();
  
  // Criação da variavél que indica que o cômodo tem alguma imagem 
  var temImagem = !(inputQtdeFilha == null)

  // Popula as colunas da lista com os itens
  for (var i = 0; i < item.length; i++) {

    var cel = row.insertCell(i);
    
    if (i == 1) {
    
      // Cria um checkbox na segunda coluna da lista
      let chk = document.createElement("INPUT");
      chk.setAttribute("type", "checkbox");
      chk.className = "selectcomodo";
      chk.id = "idselectcomodo";
      
      if (temImagem) 
      {
        // Se o cômodo tiver uma imagem, o checkbox aparece 
        chk.style.display = "block"
      }
      else 
      {
        // Se o cômodo não tiver uma imagem, o checkbox não aparece 
        chk.style.display = "none"
      }
      cel.appendChild(chk);
    }
    else
      cel.textContent = item[i];
  }

  // Chama a função que cria o botão de excluir item
  insertButton(row.insertCell(-1), "closecomodo", temImagem)
  
  // Chama a função que cria a função de excluir um item da lista
  removeComodo("closecomodo")
  
  // Chama a função que cria a função de selecionar os itens filhos do cômodo
  selectComodo()

}

/*
  --------------------------------------------------------------------------------------
  Função para remover um item da lista de acordo com o click no botão close
  --------------------------------------------------------------------------------------
*/
const removeComodo = (objetName) => {

   // Cria o objeto span
  let close = document.getElementsByClassName(objetName);
  
  // Cria o contador
  let i;

  // Faz um loop com todos os objetos de exclusão
  for (i = 0; i < close.length; i++) {

    // Cria a funçao de exclusão
    close[i].onclick = function () 
    {
      // Cria o objeto div
      let div = this.parentElement.parentElement;
    
      // Pega o id do item
      let idItem = div.getElementsByTagName('td')[0].innerHTML
    
      if (confirm("Você tem certeza?")) 
      {
        // Remove div
        div.remove()
      
        // Chama a função de deleta o item de id idItem 
        deleteItem(idItem, objetName)
        alert("Item removido!")

        // Carrega a página novamente
        //document.location.reload()


        // Carga do imovel
/*        Imovel('imoveis','imovel') */


        // Tratamento para montar as listas carregadas após a exclusão
        if (QtdeComodoCorrente>1)
        {
          ImovelCorrenteByComodo = ImovelCorrente
          document.getElementById("idselectimovel").onclick()
        }
        else
          document.getElementById("idselectimobiliaria").onclick()
        
        ImovelCorrenteByComodo = 0
        QtdeComodoCorrente=0

        // Carga do tipo de cômodo
        Tipo('tipos_comodos','tipo_comodo') 

      }
    }

  }
}

/*
  --------------------------------------------------------------------------------------
   Função para criar a função de selecionar os itens filhos do cômodo
  --------------------------------------------------------------------------------------
*/
const selectComodo = () => {

  // Cria o objeto select
  let select = document.getElementsByClassName("selectcomodo");

   // Cria o contador
  let i;

  // Faz um loop com todos os objetos de seleção
  for (i = 0; i < select.length; i++) {

  // Cria a função de seleção
    select[i].onclick = function () 
    {
    
      // Cria o objeto div
      let div = this.parentElement.parentElement;

          // Pega o id do item
      const idItem =  div.getElementsByTagName('td')[0].innerHTML

       // Cria o evento de click
      div.addEventListener('click', (event) => {

        // Faz uma pesquisa para trazer todos o checkbox que estão selecionados
        let checkboxes = document.querySelectorAll('input[class="selectcomodo"]:checked');

        // faz um lop com os checkbox selecionados
        checkboxes.forEach((checkbox) => 
        {
          // Pega o id do checkbox selecionado
          let curChk = checkbox.parentElement.parentElement.innerHTML[4];
          
          if (curChk != idItem) {

            // Caso o id do checkbox selecionado for diferente do atual, eu desmarco ele
            checkbox.checked = false
            return false;
          }
          //values.push(checkbox.value);
        }
        );
        //alert(values);
      });

      if (this.checked ||  ComodoCorrenteByImagem!=0)
      {
        // Se o item atual estiver marcado, 
        // chama a função que carrega a imagem
        if (ComodoCorrenteByImagem!=0)
          ImagemByComodo(ComodoCorrenteByImagem);
        else
          ImagemByComodo(idItem);
      }
      else 
      {
        // Se o item atual nãa estiver marcado, limpa a lista da imagem
        // e chama a função que limpa a imagem
        let table = document.getElementById("imagem");
        
        table.style.display = "none";
        for (var i = 1; i < table.rows.length;) {
          table.deleteRow(i);
        }

        ImagemByComodo(0);
      }


    }

  }
}

/*
  --------------------------------------------------------------------------------------
  Função para abrir ou fechar o formulário do cômodo e montar ou zerar o DropdownList 
  dos cômodos
  --------------------------------------------------------------------------------------
*/

const formComodo = (tipo) => {

  // Se a opção for 'O' abre o formulário
  if (tipo=='O')
    document.getElementById("formComodo").style.display = "block"
  else
    document.getElementById("formComodo").style.display = "none"

  // Chama a função que monta o DropdownList com a relação das imóveis para os comôdos
  dynamicDropdownListImovel(tipo)
  
  // Chama a função que monta o DropdownList com a relação das tipo de comôdos
  dynamicDropdownListTipoComodo(tipo)
  
}

/*
  --------------------------------------------------------------------------------------
  Função para obter a lista existente do servidor via requisição GET
  --------------------------------------------------------------------------------------
*/
const ImagemByComodo = async (id_comodo) => {

  let url = window.URL + '/imagensByComodo?id_comodo=' + id_comodo;

  ComodoCorrente = id_comodo
  console.log("ComodoCorrente = "+ComodoCorrente)
  

  var table = document.getElementById("imagem");

   // Limpando a lista das imagens
  for (var i = 1; i < table.rows.length;) {

    table.deleteRow(i);
  }

  if (id_comodo != 0) {

    // Mostrando a lista da imagem
    table.style.display = "block";
    
    fetch(url, {
      method: 'get',
    })
      .then((response) => response.json())
      .then((data) => {

        QtdeImagemCorrente = data.imagens.length

        data.imagens.forEach(
          item => insertImagemList(
            item.id,
            item.comodo,
            item.descricao
          ))
      })
      .catch((error) => {
        console.error('Error:', error);
      });
  }
}


/*
  --------------------------------------------------------------------------------------
  Função  que monta o DropdownList com a relação das tipo de comôdos
  --------------------------------------------------------------------------------------
*/
const dynamicDropdownListTipoComodo = async (tipo) => {

   // Captura dos campos
  var comodoNewTipoComodo = document.getElementById("comodoNewTipoComodo");
  var comodoNewTipoComodoId = document.getElementById("comodoNewTipoComodoId");

  if (tipo=="O")// Opção para carregar a lista
  {
    // Cria a url
    let url = window.URL + '/tipos_comodos';

    // Faz a chamada da requisição POST no servidor
    fetch(url, {
      method: 'get',
    })
      .then((response) => response.json())
      .then((data) => {

        tipos = data.tipos_comodos

        // Monta a primeira linha em branco
        let option = document.createElement("option");
        let optionText = document.createTextNode("");

        option.setAttribute('value', 0);
        option.appendChild(optionText);
        comodoNewTipoComodo.appendChild(option);

        // Popula as demais linhas
        for (var i = 0; i < tipos.length; i++) {

          let option = document.createElement("option");
          let optionText = document.createTextNode(tipos[i].descricao);

          option.setAttribute('value', tipos[i].id);
          option.appendChild(optionText);
          comodoNewTipoComodo.appendChild(option);
        }

        // Cria o evento de selecionar o item
        comodoNewTipoComodo.addEventListener("change", e => {
          comodoNewTipoComodoId.value = e.target.value;
        })


      })
      .catch((error) => {
        console.error('Error:', error);
      });
    }
    else{
      // Opção para limpar a lista
      while (comodoNewTipoComodo.hasChildNodes()) {
        comodoNewTipoComodo.removeChild(comodoNewTipoComodo.firstChild);
      }
    }
}

/*
  --------------------------------------------------------------------------------------
  --------------------------------------------------------------------------------------
  
  Funcões para tratamento da imagem do cômodo

  --------------------------------------------------------------------------------------
  --------------------------------------------------------------------------------------
*/

/*
  --------------------------------------------------------------------------------------
  Função para adicionar os campos da imagem do cômodo
  --------------------------------------------------------------------------------------
*/

const newImagem =() => 
{
  // Captura dos campos
  let inputComodo = document.getElementById("imagemNewComodoId").value;
  let inputImagem = document.getElementById("image").value;

  
  // Validação do cômodo
  if (inputComodo === undefined || inputComodo === '' || inputComodo === '0') {
   alert("Informe o cômodo!");
  } 
  else
    // Validação do tipo do cômodo 
    if (inputImagem === '') {
      alert("Informe a imagem!");
    } 

  else 
    {

    ComodoSelecionado = inputComodo
    const form = document.getElementById("formImagem");
    const formData = new FormData(form);

    // Cria a url
    let url = window.URL + '/imagem';

    // Faz a chamada da requisição POST no servidor
    fetch(url, {
      method: "POST",
      enctype: "multipart/form-data",
      body: formData
    })
      //.then(response => response.text())
      .then((response) => response.json())
      .catch(error => {
        console.error('Error:', error);
      });

      alert("Item adicionado!")

      // Limpa os campos do formulário
      document.getElementById("imagemNewComodoId").value=""
      document.getElementById("image").value=""
      document.getElementById("imagemNewDescricao").value=""
      
      // Fecha o formulário
      formImagem('C')
    
      // Tratamento para montar as listas carregadas após a inclusão
      if (QtdeImagemCorrente==0)
      {
        ImovelCorrenteByComodo  = ImovelCorrente
        document.getElementById("idselectimovel").onclick()
      }
      else
      {
        if (ComodoSelecionado!=ComodoCorrente){
          //document.getElementById("idselectimovel").onclick()

          ImovelCorrenteByComodo = ImovelSelecionado
          document.getElementById("idselectimovel").onclick()
/*           if (ComodoCorrente!=0)
          {
            ComodoCorrenteByImagem = ComodoSelecionado
            document.getElementById("idselectcomodo").onclick()
          } */      
         // else 
         //   document.getElementById("idselectimovel").onclick()
          
        }
        else{        
          if (ComodoCorrente!=0)
          {
            ComodoCorrenteByImagem = ComodoCorrente
            document.getElementById("idselectcomodo").onclick()
          }      
          else
            document.getElementById("idselectimovel").onclick()
        }
    }
      ComodoCorrenteByImagem = 0
      QtdeImagemCorrente = 0
    }
  }

/*
  --------------------------------------------------------------------------------------
  Função para inserir items na lista apresentada
  --------------------------------------------------------------------------------------
*/

const insertImagemList = (
  id,
  inputComodo,
  inputDescricao
) => {
  var item = [
    id,
    "",
    inputComodo,
    inputDescricao
  ]

  var table = document.getElementById("imagem");
  var row = table.insertRow();

  for (var i = 0; i < item.length; i++) {
    var cel = row.insertCell(i);

    if (i == 1) {
      const img = document.createElement("img");
      img.src = window.URL + `/retornar_imagem?id=${item[0]}`;

      const tdImagem = document.createElement("td");
      tdImagem.appendChild(img);

      cel.appendChild(img)
    }
    else {

      cel.textContent = item[i];
    }
  }

  insertButton(row.insertCell(-1), "closeimagem", false)
  removeImage("closeimagem")
  selectComodo()

}

/*
  --------------------------------------------------------------------------------------
  Função para remover um item da lista de acordo com o click no botão close
  --------------------------------------------------------------------------------------
*/
const removeImage = (objetName) => {

  // Cria o objeto span
 let close = document.getElementsByClassName(objetName);
 
 // Cria o contador
 let i;

 // Faz um loop com todos os objetos de exclusão
 for (i = 0; i < close.length; i++) {

   // Cria a funçao de exclusão
   close[i].onclick = function () 
   {
     // Cria o objeto div
     let div = this.parentElement.parentElement;
   
     // Pega o id do item
     let idItem = div.getElementsByTagName('td')[0].innerHTML
   
     if (confirm("Você tem certeza?")) 
     {
       // Remove div
       div.remove()
     
       // Chama a função de deleta o item de id idItem 
       deleteItem(idItem, objetName)
       alert("Item removido!")

       // Limpa os campos do formulário
       document.getElementById("imagemNewComodoId").value=""
       document.getElementById("image").value=""
       document.getElementById("imagemNewDescricao").value=""
       
       // Fecha o formulário
       formImagem('C')
     
       // Tratamento para montar as listas carregadas após a exclusão
       if (QtdeImagemCorrente>1)
       {
          ComodoCorrenteByImagem = ComodoCorrente
          document.getElementById("idselectcomodo").onclick()
        }
        else
          document.getElementById("idselectimovel").onclick()
        
        ComodoCorrenteByImagem = 0
        QtdeImagemCorrente = 0
       
     
     }
   }

 }
}

/*
  --------------------------------------------------------------------------------------
  Função para abrir ou fechar o formulário da imagem do cômodo e montar ou zerar o 
  DropdownList dos cômodos
  --------------------------------------------------------------------------------------
*/

const formImagem = (tipo) => {

  // Se a opção for 'O' abre o formulário
  if (tipo=='O')
    document.getElementById("formImagem").style.display = "block"
  else
    document.getElementById("formImagem").style.display = "none"

  // Chama a função que monta o DropdownList com a relação das coômodos para as imagens
  dynamicDropdownListComodo(tipo)
  
}

/*
  --------------------------------------------------------------------------------------
  Função  que monta o DropdownList com a relação dos comôdos
  --------------------------------------------------------------------------------------
*/
const dynamicDropdownListComodo = async (tipo) => {

  // Captura dos campos
  var imagemNewComodo = document.getElementById("imagemNewComodo");
  var imagemNewComodoId = document.getElementById("imagemNewComodoId");

  if (tipo=="O") // Opção para carregar a lista
  {
    // Cria a url
    let url = window.URL + '/comodosByImovel?id_imovel=' + ImovelCorrente;

    // Faz a chamada da requisição POST no servidor
    fetch(url, {
      method: 'get',
    })
      .then((response) => response.json())
      .then((data) => {

        tipos = data.comodos

        // Monta a primeira linha em branco
        let option = document.createElement("option");
        let optionText = document.createTextNode("");

        option.setAttribute('value', 0);
        option.appendChild(optionText);
        imagemNewComodo.appendChild(option);

        // Popula as demais linhas
        for (var i = 0; i < tipos.length; i++) {

          let option = document.createElement("option");
          let optionText = document.createTextNode(tipos[i].nome);

          option.setAttribute('value', tipos[i].id);
          option.appendChild(optionText);
          imagemNewComodo.appendChild(option);

        }

        // Cria o evento de selecionar o item
        imagemNewComodo.addEventListener("change", e => {
          imagemNewComodoId.value = e.target.value;
        })

      })
      .catch((error) => {
        console.error('Error:', error);
      });
    }
    else{
      // Opção para limpar a lista
      while (imagemNewComodo.hasChildNodes()) {
        imagemNewComodo.removeChild(imagemNewComodo.firstChild);
      }
    }
}
