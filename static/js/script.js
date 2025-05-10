// Avatar selection - and attribute value to input name 'gender'
document.addEventListener("DOMContentLoaded", function () {
    const genderInput = document.getElementById("gender");
    const femaleAvatar = document.getElementById("female-avatar");
    const maleAvatar = document.getElementById("male-avatar");

    femaleAvatar.addEventListener("click", function () {
      genderInput.value = "female";
    });

    maleAvatar.addEventListener("click", function () {
      genderInput.value = "male";
    });
});


// Add the partials/card.html inside cardContainer
document.querySelector('#cardForm').addEventListener('submit', async function (e) {
    e.preventDefault();
    const name = document.querySelector('#cardInput').value;

    const response = await fetch('dashboard', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ name }) // {'name': name}
    });

    const data = await response.json();
    if (response.ok) {
        document.querySelector('#cardContainer').insertAdjacentHTML('beforeend', data.html);

        const addedElement = document.querySelector('#cardContainer').lastElementChild;
        addedElement.scrollIntoView({ behavior: 'smooth', block: 'center' });
    } else {
        console.log(data.error);
    }

    document.querySelector('#cardInput').value = '';
});


// Delete pokemon by removing the card.html that has the equivalent id
async function deletePokemon(id) {
  try {
      const res = await fetch('delete_pokemon/' + id, {
          method: 'DELETE'
      });

      if (res.ok) {
          document.getElementById('card-' + id).remove();
      } else {
          alert('Erro ao deletar Pokémon.');
      }
  } catch (error) {
      console.error('Erro:', error);
  }
}

// Add a random pokemon - same from 
async function randomPokemon() {
    const response = await fetch('random_pokemon', {
        method: 'POST'
    });

    const data = await response.json();
    if (response.ok) {
        // Agora insere HTML seguro renderizado no servidor
        document.querySelector('#cardContainer').insertAdjacentHTML('beforeend', data.html);

        const addedElement = document.querySelector('#cardContainer').lastElementChild;
        addedElement.scrollIntoView({ behavior: 'smooth', block: 'center' });

      } else {
        console.log(data.error);
    }
}

// Clear all the cards that was added inside cardContainer
async function clearPokemon() {
  const response = await fetch('clear_pokemon', {
    method: 'POST'
  });

  const data = await response.json();
  if (response.ok) {
    document.querySelector('#cardContainer').innerHTML = '';
  }
  else {
    console.log(data.error)
  }
}

// Function to remove the flash messages when user reload the page
window.addEventListener("beforeunload", function () {
  const flash = document.getElementById("flash-message");
 
  if (flash) flash.remove();
});


console.log('Javascript loaded successfully')
