class ModalInformation{
    constructor(modal){
        this.modal = modal;
        this.btn_close = this.modal.querySelector('#btn-close-modal-information');
        this.btn_close.addEventListener('click', () => this.hide());
        this.steps = [...this.modal.querySelectorAll('.step')];
        this.loader = this.modal.querySelector('#loader');
        this.error_section = this.modal.querySelector('#modal-error-section');
        this.error_message = this.modal.querySelector('#modal-error-message');
    }
    show(){
        this.modal.classList.remove('hidden');
        this.#closeError();
    }
    hide(){
        this.modal.classList.add('hidden');
    }
    #clearSteps(){
        this.steps.forEach(step => {
            step.classList.remove('current');
        });
    }
    setStep(step){
        if (step > this.steps.length+1) return;
        this.#clearSteps();
        this.steps[step-1].classList.add('current');
        if (step == this.steps.length){
            this.modal.classList.add('completed');
        }
    }
    notifyError(error){
        this.error_section.classList.remove('hidden');
        
    }
    #closeError(){
        this.error_section.classList.add('hidden');
    }
}


const modalInformation = new ModalInformation(document.getElementById('modal-information'));
export {modalInformation};