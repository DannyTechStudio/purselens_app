/*--------------------------------------------------------
        DOM ELEMENTS LOADED
-----------------------------------------------------------*/
document.addEventListener('DOMContentLoaded', () => {
    
    const messageDisplay = document.querySelector('.message-display');
    const categoryCardContainer = document.getElementById('category-card-container');

    //---------- Category Card Elements Creation
    function createCategoryCard(category) {
        const categoryCard = document.createElement('div');
        const cardHeader = document.createElement('div');
        const categoryType = document.createElement('span');
        const actionMenu = document.createElement('div');
        const actionTrigger = document.createElement('button');
        const actionDropDown = document.createElement('ul');
        const categoryTitle = document.createElement('h3');
        const categoryDescription = document.createElement("p");

        categoryType.textContent = category.type;
        categoryTitle.textContent = category.name;
        categoryDescription.textContent = category.short_description;

        categoryCard.classList.add('category-card');
        cardHeader.classList.add('card-header');
        categoryType.classList.add('category-type');
        
        
        if (categoryType.textContent === 'transfer') {
            categoryType.classList.add('transfer');
        }
        
        if (categoryType.textContent === 'income') {
            categoryType.classList.add('income');
        }
        
        if (categoryType.textContent === 'expense') {
            categoryType.classList.add('expense');
        }
        
        actionMenu.classList.add('action-menu');
        
        actionTrigger.classList.add('action-trigger');
        actionTrigger.setAttribute('aria-expanded', 'false');
        actionTrigger.setAttribute('aria-haspopup', 'true');
        
        actionDropDown.classList.add('action-dropdown');
        actionDropDown.setAttribute('role', 'menu');

        categoryTitle.classList.add('category-title');
        categoryDescription.classList.add('category-desc');
        
        actionTrigger.innerHTML = `
            <span class="chevron">
                <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-three-dots-vertical" viewBox="0 0 16 16">
                    <path d="M9.5 13a1.5 1.5 0 1 1-3 0 1.5 1.5 0 0 1 3 0m0-5a1.5 1.5 0 1 1-3 0 1.5 1.5 0 0 1 3 0m0-5a1.5 1.5 0 1 1-3 0 1.5 1.5 0 0 1 3 0"/>
                </svg>
            </span>
        `;

        actionDropDown.innerHTML = `
            <li>
                <button class="action-btn edit" role="menuitem" data-action="edit">
                    <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-pen" viewBox="0 0 16 16">
                        <path d="m13.498.795.149-.149a1.207 1.207 0 1 1 1.707 1.708l-.149.148a1.5 1.5 0 0 1-.059 2.059L4.854 14.854a.5.5 0 0 1-.233.131l-4 1a.5.5 0 0 1-.606-.606l1-4a.5.5 0 0 1 .131-.232l9.642-9.642a.5.5 0 0 0-.642.056L6.854 4.854a.5.5 0 1 1-.708-.708L9.44.854A1.5 1.5 0 0 1 11.5.796a1.5 1.5 0 0 1 1.998-.001m-.644.766a.5.5 0 0 0-.707 0L1.95 11.756l-.764 3.057 3.057-.764L14.44 3.854a.5.5 0 0 0 0-.708z"/>
                    </svg>
                    <span>Edit Category</span>
                </button>
            </li>

            <li>
                <button class="action-btn delete" role="menuitem" data-action="delete">
                    <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="lucide lucide-trash preview-icon">
                        <path d="M10 11v6"/><path d="M14 11v6"/><path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6"/><path d="M3 6h18"/><path d="M8 6V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"/>
                    </svg>
                    <span>Delete Category</span>
                </button>
            </li>
        `;

        actionMenu.append(actionTrigger, actionDropDown);
        cardHeader.append(categoryType, actionMenu);
        categoryCard.append(
            cardHeader,
            categoryTitle,
            categoryDescription,
        );

        // categoryCardContainer.appendChild(categoryCard);

        return { categoryCard, actionTrigger, actionDropDown };
    }


    //---------- Category Card Behavior
    function bindCategoryCard({ actionTrigger, actionDropDown }, category, { onEdit, onDelete }) {

        actionTrigger.addEventListener('click', (e) => {
            e.stopPropagation();    // stops document listener from closing it immediately
            const isOpen = actionDropDown.classList.toggle('open');
            actionTrigger.setAttribute('aria-expanded', String(isOpen));
        });

        // Single listener on the dropdown for its buttons (event delegation)
        actionDropDown.addEventListener('click', (e) => {
            const btn = e.target.closest('[data-action]');
            if (!btn) return;       // click might have landed on the <ul> gap - not a button

            // Close dropdown before actions
            actionDropDown.classList.remove('open');
            actionTrigger.setAttribute('aria-expanded', 'false');

            if (btn.dataset.action === 'edit') onEdit(category);
            if (btn.dataset.action === 'delete') onDelete(category);
        });
    }


    //---------- Function Orchestrator
    function buildCategoryCard(category, handlers) {
        const references = createCategoryCard(category);
        bindCategoryCard(references, category, handlers);

        return references.categoryCard
    }


    //---------- Card Render
    function renderCategories(categories) {
        categoryCardContainer.innerHTML = '';

        if (!categories || categories.length === 0) {
            categoryCardContainer = `
                <p class="empty-category-state">No categories available.</p>
            `;

            return;
        }

        categories.forEach(category => {
            const card = buildCategoryCard(category, {
                onEdit: (cat) => openEditModal(cat),
                onDelete: (cat) => handleDeleteCategory(cat),
            });
            categoryCardContainer.appendChild(card);
        });
    }


    //------------- Edit Handler
    function openEditModal(category) {
        const modal = document.getElementById('category-modal-overlay');
        const modalHeading = document.querySelector('modal-heading');
        const nameInput = document.getElementById('category-name-input');
        const typeSelect = document.getElementById('category-type-dropdown');

        // Populate the existing form with current values;
        nameInput.value = category.name;
        typeSelect.value = category.type;

        // Flag the modal as being in edit mode and remember which category is being edited - using their ID
        modal.dataset.mode   = 'edit';
        modal.dataset.editId = category.id;
        modalHeading.textContent  = 'Edit Category';

        modal.style.display = 'flex';
        document.body.classList.add('modal-open');
    }


    //-------------- On modal closure or cancellation, reset it back to create mode
    function resetCategoryModal() {
        const modal = document.getElementById('category-modal-overlay');
        const modalHeading = modal.querySelector('modal-heading');
        const form = modal.querySelector('.category-form');

        modal.dataset.mode   = 'create';
        modal.dataset.editId = '';
        modalHeading.textContent  = 'Add Category';
        form.reset();

        modal.style.display = 'none';
        document.body.classList.remove('modal-open');
    }


    //------------- Form Submission
    const categoryForm = document.querySelector('.category-form');

    if (categoryForm) {
        categoryForm.addEventListener('submit', async (e) => {
            e.preventDefault();

            const modal = document.getElementById('category-modal-overlay');
            const isEdit = modal.dataset.mode === 'edit';
            const editId = modal.dataset.editId;

            const payload = {
                name: document.getElementById('category-name-input').value,
                type: document.getElementById('category-type-dropdown').value
            };

            try {

                if (isEdit) {
                    response = await apiPatch(`/categories/${editId}`, payload);
                } else {
                    response = await apiPost(`/categories/`, payload);
                }

                messageDisplay.textContent = response.message;
                messageDisplay.classList.add('success');
                messageDisplay.style.display = "flex";
                
                setTimeout(() => {
                    messageDisplay.textContent = "";
                    messageDisplay.classList.remove('success');
                    messageDisplay.style.display = "none";
                }, 3000);

                resetCategoryModal();
                loadCategories();

            } catch (error) {
                console.error('Save failed', error.message);

                messageDisplay.textContent = response.message;
                messageDisplay.classList.add('error');
                messageDisplay.style.display = "flex";
                
                setTimeout(() => {
                    messageDisplay.textContent = "";
                    messageDisplay.classList.remove('error');
                    messageDisplay.style.display = "none";
                }, 3000);
            }
        });
    }


    //-------- Category Deletion Handler
    async function handleDeleteCategory(category) {
        const confirmed = confirm(`Delete "${category.name}"? This cannot be updone.`);
        if (!confirmed) return;

        try { 
            const response = await apiDelete(`/categories/${category.id}`);

            messageDisplay.textContent = response.message;
            messageDisplay.classList.add('success');
            messageDisplay.style.display = "flex";
            
            setTimeout(() => {
                messageDisplay.textContent = "";
                messageDisplay.classList.remove('success');
                messageDisplay.style.display = "none";
            }, 3000);

            loadCategories();  // re-fetch and re-render

        } catch (error) {
            console.error('Deletion failed', error.message);

            messageDisplay.textContent = response.message;
            messageDisplay.classList.add('error');
            messageDisplay.style.display = "flex";
            
            setTimeout(() => {
                messageDisplay.textContent = "";
                messageDisplay.classList.remove('error');
                messageDisplay.style.display = "none";
            }, 3000);
        }
    }

    //------------- OUTSIDE CLICK — document level, set up once 
    document.addEventListener('click', () => {
        document.querySelectorAll('.action-dropdown.open').forEach(dropdown => {
            dropdown.classList.remove('open');
            dropdown.previousElementSibling.setAttribute('aria-expanded', 'false');
        });
    });


    async function loadCategories() {
        try {

            const response = await apiGet('/categories/');
            renderCategories(response.data.results);

            messageDisplay.textContent = response.message;
            messageDisplay.classList.add('success');
            messageDisplay.style.display = "flex";
            
            setTimeout(() => {
                messageDisplay.textContent = "";
                messageDisplay.classList.remove('success');
                messageDisplay.style.display = "none";
            }, 3000);

        } catch (error) {
            console.error("Categories error:", error);
            
            messageDisplay.textContent = error.message;
            messageDisplay.classList.add('error');
            messageDisplay.style.display = "flex";
            
            setTimeout(() => {
                messageDisplay.textContent = "";
                messageDisplay.classList.remove('error');
                messageDisplay.style.display = "none";
            }, 3000);
        }
    }

    loadCategories();

    // Insight rendering
    const insightsData = JSON.parse(
        sessionStorage.getItem('Dashboard Insights')
    );

    function renderInsights(insights) {
        const insightsContainer = document.querySelector('.insight-wrapper');

        insightsContainer.innerHTML = '';

        if (!insights || insights.length === 0) {
            insightsContainer.innerHTML = `
                <p class="empty-insight-state">No insights yet. Start tracking your spending to see trends.</p>
            `;
        }

        insights.forEach(insight => {
            const insightBlock = document.createElement('div');
            const insightLabel = document.createElement('span');
            const insightTitle = document.createElement('h2');
            const insightMsg = document.createElement('p');

            insightBlock.classList.add('insight-block');

            insightLabel.classList.add('insight-label');
            insightLabel.textContent = insight.type;

            insightTitle.textContent = insight.title;
            insightTitle.classList.add("insight-heading");
            
            insightMsg.textContent = insight.message
            insightMsg.classList.add('insight-message');

            if (insightLabel.textContent === 'info') {
                insightLabel.classList.add('info-type');
                insightBlock.classList.add('info-type');
            }
            
            if (insightLabel.textContent === 'success') {
                insightLabel.classList.add('success-type');
                insightBlock.classList.add('success-type');
            }

            if (insightLabel.textContent === 'warning') {
                insightLabel.classList.add('warning-type');
                insightBlock.classList.add('warning-type');
            }

            if (insightLabel.textContent === 'critical') {
                insightLabel.classList.add('critical-type');
                insightBlock.classList.add('critical-type');
            }

            insightBlock.append(
                insightLabel,
                insightTitle,
                insightMsg,
            );

            insightsContainer.appendChild(insightBlock);
        });
    }

    renderInsights(insightsData);
    

});