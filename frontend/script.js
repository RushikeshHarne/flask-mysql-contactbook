const apiUrl = "http://127.0.0.1:5000/contacts";

document.getElementById("contactForm").addEventListener("submit", async function (e) {
  e.preventDefault();
  const id = document.getElementById("contactId").value;
  const contact = {
    name: document.getElementById("name").value,
    email: document.getElementById("email").value,
    phone: document.getElementById("phone").value,
  };

  if (id) {
    await fetch(`${apiUrl}/${id}`, {
      method: "PUT",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(contact),
    });
  } else {
    await fetch(apiUrl, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(contact),
    });
  }

  document.getElementById("contactForm").reset();
  loadContacts();
});

async function loadContacts() {
  const res = await fetch(apiUrl);
  const contacts = await res.json();

  const tbody = document.getElementById("contactList");
  tbody.innerHTML = "";

  contacts.forEach(contact => {
    const row = document.createElement("tr");
    row.innerHTML = `
      <td>${contact.name}</td>
      <td>${contact.email}</td>
      <td>${contact.phone}</td>
      <td>
        <button onclick="editContact(${contact.id})">Edit</button>
        <button onclick="deleteContact(${contact.id})">Delete</button>
      </td>
    `;
    tbody.appendChild(row);
  });
}

async function editContact(id) {
  const res = await fetch(`${apiUrl}/${id}`);
  const contact = await res.json();

  document.getElementById("contactId").value = contact.id;
  document.getElementById("name").value = contact.name;
  document.getElementById("email").value = contact.email;
  document.getElementById("phone").value = contact.phone;
}

async function deleteContact(id) {
  await fetch(`${apiUrl}/${id}`, { method: "DELETE" });
  loadContacts();
}

loadContacts();
