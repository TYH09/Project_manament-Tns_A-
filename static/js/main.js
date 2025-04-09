// Confirmar eliminación de tarea
function confirmDelete(event) {
    if (!confirm('Are you sure you want to delete this project??')) {
        event.preventDefault();
    }
}

document.addEventListener('DOMContentLoaded', function() {
    const today = new Date();
    const dueDates = document.querySelectorAll('.due-date');
    
    dueDates.forEach(date => {
        const dueDate = new Date(date.dataset.date);
        const diffDays = Math.ceil((dueDate - today) / (1000 * 60 * 60 * 24));
        
        if (diffDays < 0) {
            date.classList.add('text-danger'); 
        } else if (diffDays <= 3) {
            date.classList.add('text-warning'); 
        } else {
            date.classList.add('text-success');
        }
    });
});


document.getElementById('category-filter')?.addEventListener('change', function() {
    const category = this.value;
    const projects = document.querySelectorAll('.project-card');
    
    projects.forEach(project => {
        if (category === 'all' || project.dataset.category === category) {
            project.style.display = 'block';
        } else {
            project.style.display = 'none';
        }
    });
});


const completeButtons = document.querySelectorAll('.complete-project');
completeButtons.forEach(button => {
    button.addEventListener('click', function(e) {
        e.preventDefault();
        const projectCard = this.closest('.card');
        projectCard.style.transition = 'all 0.3s';
        projectCard.style.opacity = '0.5';
        projectCard.style.transform = 'scale(0.95)';
        
        setTimeout(() => {
            window.location.href = this.href;
        }, 300);
    });
});
