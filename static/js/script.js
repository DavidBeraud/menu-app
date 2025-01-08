// Fonction pour charger les données des ingrédients depuis le fichier JSON
async function loadIngredients() {
    try {
        const response = await fetch('/static/data/ingredients.json'); // Chemin correct
        if (!response.ok) {
            throw new Error('Erreur lors du chargement des ingrédients');
        }
        const data = await response.json();
        console.log('Données chargées:', data); // Log pour vérifier
        return data.ingredients;
    } catch (error) {
        console.error('Erreur:', error);
        alert('Impossible de charger les ingrédients. Veuillez réessayer plus tard.');
        return {};
    }
}

// Fonction pour remplir le menu déroulant des ingrédients
function fillIngredientSelect(selectElement, ingredientsData) {
    // Vider le menu déroulant avant de le remplir
    selectElement.innerHTML = '';

    // Ajouter une option par défaut
    const defaultOption = document.createElement('option');
    defaultOption.value = '';
    defaultOption.textContent = 'Sélectionnez un ingrédient';
    defaultOption.disabled = true;
    defaultOption.selected = true;
    selectElement.appendChild(defaultOption);

    // Ajouter les options par catégorie
    for (const [category, items] of Object.entries(ingredientsData)) {
        const optgroup = document.createElement('optgroup');
        optgroup.label = category;

        items.forEach(item => {
            const option = document.createElement('option');
            option.value = item;
            option.textContent = item;
            optgroup.appendChild(option);
        });

        selectElement.appendChild(optgroup);
    }

    console.log('Menu déroulant rempli:', selectElement); // Log pour vérifier
}

// Fonction pour initialiser la gestion des ingrédients
async function setupIngredients() {
    const container = document.getElementById('ingredients-container');
    const addButton = document.getElementById('ajouter-ingredient');
    const template = document.getElementById('ingredient-template');

    if (!container || !addButton || !template) {
        console.error('Élément manquant pour les ingrédients');
        return;
    }

    // Charger les ingrédients depuis le fichier JSON
    const ingredientsData = await loadIngredients();
    console.log('Ingrédients chargés:', ingredientsData); // Log pour vérifier

    // Ajouter un nouvel ingrédient
    addButton.addEventListener('click', () => {
        const newItem = template.content.cloneNode(true);

        // Remplir le menu déroulant des ingrédients
        const ingredientSelect = newItem.querySelector('select[name="ingredient_nom[]"]');
        if (ingredientSelect) {
            fillIngredientSelect(ingredientSelect, ingredientsData);
        }

        // Gestion de la suppression d'un champ d'ingrédient
        const supprimerButton = newItem.querySelector('.supprimer-ingredient');
        supprimerButton.addEventListener('click', function () {
            container.removeChild(supprimerButton.closest('.ingredient'));
        });

        container.appendChild(newItem);

        console.log('Nouvel ingrédient ajouté:', newItem); // Log pour vérifier
    });

    // Supprimer un ingrédient existant
    container.addEventListener('click', (event) => {
        if (event.target.classList.contains('supprimer-ingredient')) {
            event.target.closest('.ingredient').remove();
        }
    });
}

// Fonction pour initialiser la gestion des étapes
function setupEtapes() {
    const container = document.getElementById('etapes-container');
    const addButton = document.getElementById('ajouter-etape');
    const template = document.getElementById('etape-template');

    if (!container || !addButton || !template) {
        console.error('Élément manquant pour les étapes');
        return;
    }

    // Ajouter une nouvelle étape
    addButton.addEventListener('click', () => {
        const newItem = template.content.cloneNode(true);

        // Gestion de la suppression d'une étape
        const supprimerButton = newItem.querySelector('.supprimer-etape');
        supprimerButton.addEventListener('click', function () {
            container.removeChild(supprimerButton.closest('.etape'));
        });

        container.appendChild(newItem);

        console.log('Nouvelle étape ajoutée:', newItem); // Log pour vérifier
    });

    // Supprimer une étape existante
    container.addEventListener('click', (event) => {
        if (event.target.classList.contains('supprimer-etape')) {
            event.target.closest('.etape').remove();
        }
    });
}

// Masquer automatiquement les messages flash après 3 secondes
function setupFlashMessages() {
    const flashMessages = document.querySelectorAll('.alert');

    flashMessages.forEach(alert => {
        // Ajouter un bouton de fermeture manuelle
        const closeButton = document.createElement('button');
        closeButton.textContent = '×';
        closeButton.classList.add('close-button');
        closeButton.addEventListener('click', () => {
            alert.style.display = 'none';
        });
        alert.appendChild(closeButton);

        // Masquer l'alerte après 3 secondes
        setTimeout(() => {
            alert.style.opacity = '0';  // Appliquer un fondu
            setTimeout(() => {
                alert.style.display = 'none';  // Masquer l'élément après le fondu
            }, 500);  // Attendre 0.5 seconde pour que le fondu se termine
        }, 3000);  // Délai avant de commencer le fondu
    });
}

// Gestion de l'impression de la zone "printable-area"
function setupPrintButton() {
    const printButton = document.getElementById('print-button');
    if (printButton) {
        printButton.addEventListener('click', function () {
            // Créer une nouvelle fenêtre ou un nouvel onglet pour l'impression
            const printWindow = window.open('', '_blank');
            
            // Récupérer le contenu de la zone "printable-area"
            const printContent = document.getElementById('printable-area').innerHTML;

            // Écrire le contenu dans la nouvelle fenêtre
            printWindow.document.write(`
                <html>
                    <head>
                        <title>Menu de la semaine</title>
                        <style>
                            body { font-family: Arial, sans-serif; }
                            table { width: 100%; border-collapse: collapse; }
                            th, td { border: 1px solid #000; padding: 8px; text-align: left; }
                            th { background-color: #f2f2f2; }
                        </style>
                    </head>
                    <body>
                        ${printContent}
                    </body>
                </html>
            `);

            // Fermer le document pour finaliser le contenu
            printWindow.document.close();

            // Lancer l'impression
            printWindow.print();
        });
    }
}

// Initialisation des fonctionnalités
document.addEventListener('DOMContentLoaded', async () => {
    try {
        // Gestion des ingrédients
        await setupIngredients();

        // Gestion des étapes
        setupEtapes();

        // Masquer les messages flash après 3 secondes
        setupFlashMessages();

        // Configurer le bouton d'impression
        setupPrintButton();
    } catch (error) {
        console.error('Erreur lors de l\'initialisation:', error);
        alert('Une erreur est survenue lors du chargement de la page.');
    }
});