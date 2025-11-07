// ATENÇÃO: Esta URL será o nome do nosso "Service" do backend no Kubernetes.
// O Ingress ou um Port-forward vai nos ajudar a acessar a API de fora do cluster.
const API_URL = 'http://localhost:5000'; // Mude para o endereço do seu backend durante os testes.

const form = document.getElementById('form-contato');
const listaContatos = document.getElementById('lista-contatos');
const loadingMessage = document.getElementById('loading-message');

// Função para buscar e exibir os contatos
const fetchContatos = async () => {
    loadingMessage.style.display = 'block';
    listaContatos.innerHTML = ''; // Limpa a lista antes de carregar
    try {
        const response = await fetch(`${API_URL}/contatos`);
        if (!response.ok) {
            throw new Error(`Erro na rede: ${response.statusText}`);
        }
        const contatos = await response.json();
        
        if (contatos.length === 0) {
            loadingMessage.textContent = 'Nenhum contato encontrado.';
        } else {
            loadingMessage.style.display = 'none';
        }

        contatos.forEach(contato => {
            const li = document.createElement('li');
            li.textContent = `Nome: ${contato.nome} - Tel: ${contato.telefone}`;
            listaContatos.appendChild(li);
        });
    } catch (error) {
        console.error('Falha ao buscar contatos:', error);
        loadingMessage.textContent = 'Erro ao carregar contatos. O backend está rodando?';
    }
};

// Função para adicionar um novo contato
form.addEventListener('submit', async (event) => {
    event.preventDefault(); // Impede o recarregamento da página

    const nome = document.getElementById('nome').value;
    const telefone = document.getElementById('telefone').value;

    try {
        const response = await fetch(`${API_URL}/contato`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ nome, telefone }),
        });

        if (!response.ok) {
            throw new Error('Falha ao adicionar contato');
        }

        // Limpa o formulário e atualiza a lista
        form.reset();
        fetchContatos();

    } catch (error) {
        console.error('Erro ao salvar contato:', error);
        alert('Não foi possível salvar o contato.');
    }
});

// Carrega os contatos assim que a página é aberta
document.addEventListener('DOMContentLoaded', fetchContatos);