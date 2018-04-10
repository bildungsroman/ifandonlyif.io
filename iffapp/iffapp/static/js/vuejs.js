new Vue({
  delimiters: ['${', '}$'],
  el: '#app',
  data: {
    message: 'This is where Vue.js will do its magic!',
    ifflists_all: [],
    ifflists_current: [],
    ifflists_completed: [],
    todos_all: [],
    loading: false,
    displayedIfflist: {},
    displayedTodos: [],
    newIfflist: {'get-to-do': null, 'todo_set': null},
    newTodo: {},
  },
  http: {
    root: 'http://localhost:8000',
    headers: {
      Authorization: 'Basic YXBpOnBhc3N3b3Jk'
    }
  },
  mounted: function () {
    this.getAllTodos(); // get todos first, or else ifflists are not populated with todos
  },
  methods: {
    getAllTodos: function () {  // gets all the todos, regardless of user
      this.loading = true;
      this.$http.get('api/todoitems/')
          .then((response) => {
            this.todos_all = response.body;
            this.todos_all.sort(x => -x.id);  // sort by id number so the newest is on top
            this.getIfflists();  // get ifflists only after todos have been gotten
            this.loading = false;
          })
          .catch((err) => {
            this.loading = false;
            console.log(err);
          })
    },
    getIfflists: function () {  // gets all the ifflists for the logged-in user
      this.loading = true;
      this.$http.get('api/')
          .then((response) => {
            this.ifflists_all = response.body;
            for (let i = 0; i < response.body.length; i++) {
              if (response.body[i].is_completed === false) {
                this.ifflists_current.push(response.body[i]);
              } else {
                this.ifflists_completed.push(response.body[i]);
              }
            }
            this.ifflists_current.sort(x => x.id);  // sort by id number so the newest is on top
            this.ifflists_completed.sort(x => x.id);  // sort by id number so the newest is on top
            this.loadStarter(this.ifflists_current[0]);
            this.loading = false;
          })
          .catch((err) => {
            this.loading = false;
            console.log(err);
          })
    },
    loadStarter: function (starter) {  // loads the newest current ifflist as the starter list
      this.displayedIfflist = starter;
      console.log(this.displayedIfflist.id);
      this.getTodos(starter.id);
    },
    getIfflist: function (id) {  // loads list on click
      let add_todo_field = document.querySelector('.add_todo_field');
      add_todo_field.classList.add('hidden');
      this.loading = true;
      this.$http.get(`/api/${id}/`)
          .then((response) => {
            this.displayedIfflist = response.body;
            console.log(this.displayedIfflist.id);
            this.getTodos(this.displayedIfflist.id);
            this.loading = false;
          })
          .catch((err) => {
            this.loading = false;
            console.log(err);
          })
    },
    getTodos: function (id) {  // get the todos for the displayed ifflist
      this.displayedTodos = [];  // clear or else it just adds on todos to the wrong ifflist
      for (let i = 0; i < this.todos_all.length; i++) {
        if (this.todos_all[i].ifflist === id) {
          this.displayedTodos.push(this.todos_all[i]);
        }
      }
    },
    showAdd: function () {
      let add_todo_field = document.querySelector('.add_todo_field');
      add_todo_field.classList.remove('hidden');
    },
    addTodo: function () {
      let new_todo_item = document.querySelector('#new_todo_item').value;
      this.newTodo = {'text': new_todo_item, 'ifflist': this.displayedIfflist.id, 'is_completed': false};
      console.log(this.newTodo.text);
      console.log(this.newTodo.ifflist);
      let csrf_token = Cookies.get('csrftoken');
      this.$http.post('/api/todoitems/', this.newTodo, {headers: {'X-CSRFToken': csrf_token}})
          .then((response) => {
            this.loading = false;
            this.getIfflist(this.displayedIfflist.id);
          })
          .catch((err) => {
            this.loading = false;
            console.log(err);
          })
    },
    addIfflist: function () {
      this.loading = true;
      this.$http.post('/api/', this.newIfflist)
          .then((response) => {
            this.loading = false;
            this.getIfflists();
          })
          .catch((err) => {
            this.loading = false;
            console.log(err);
          })
    },
    updateIfflist: function () {
      this.loading = true;
      this.$http.put(`/api/${this.currentIfflist.ifflist_id}/`, this.currentIfflist)
          .then((response) => {
            this.loading = false;
            this.currentIfflist = response.data;
            this.getIfflists();
          })
          .catch((err) => {
            this.loading = false;
            console.log(err);
          })
    },
    deleteIfflist: function (id) {
      this.loading = true;
      this.$http.delete(`/api/${id}/`)
          .then((response) => {
            this.loading = false;
            this.getIfflists();
          })
          .catch((err) => {
            this.loading = false;
            console.log(err);
          })
    },
    deleteTodoItem: function (id) {
      this.loading = true;
      this.$http.delete(`/api/todoitem/${id}/`)
          .then((response) => {
            this.loading = false;
            this.getIfflists();
          })
          .catch((err) => {
            this.loading = false;
            console.log(err);
          })
    },
  },
  computed: {},

});
