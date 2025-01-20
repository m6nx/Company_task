function addOwner() {
    const ownersContainer = document.getElementById('owners-container');
    const ownerEntry = document.querySelector('.owner-entry').cloneNode(true);
    ownerEntry.querySelectorAll('input').forEach(input => input.value = "");
    ownersContainer.appendChild(ownerEntry);
}

function removeOwner() {
    const ownersContainer = document.getElementById('owners-container');
    if (ownersContainer.children.length > 1) {
        ownersContainer.removeChild(ownersContainer.lastChild);
    }
}