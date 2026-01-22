import api from "./api";

export const userService = {
  list() {
    return api.get("/users/");
  },

  get(id) {
    return api.get(`/users/${id}`);
  },

  create(payload) {
    return api.post("/users/", payload);
  },

  update(id, payload) {
    return api.put(`/users/${id}`, payload);
  },

  delete(id) {
    return api.delete(`/users/${id}`);
  },
};
