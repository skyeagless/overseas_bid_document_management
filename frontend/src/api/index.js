import axios from 'axios'

const api = axios.create({
  baseURL: '/api',
  timeout: 10000
})

export default {
  getTenderFiles() {
    return api.get('/tender-files')
  },
  createTenderFile(data) {
    return api.post('/tender-files', data)
  },
  getTenderFile(id) {
    return api.get(`/tender-files/${id}`)
  },
  updateTenderFile(id, data) {
    return api.put(`/tender-files/${id}`, data)
  },
  deleteTenderFile(id) {
    return api.delete(`/tender-files/${id}`)
  },

  getProjectRecords() {
    return api.get('/project-records')
  },
  createProjectRecord(data) {
    return api.post('/project-records', data)
  },
  getProjectRecord(id) {
    return api.get(`/project-records/${id}`)
  },
  updateProjectRecord(id, data) {
    return api.put(`/project-records/${id}`, data)
  },
  deleteProjectRecord(id) {
    return api.delete(`/project-records/${id}`)
  },

  getPersonnel() {
    return api.get('/personnel')
  },
  createPersonnel(data) {
    return api.post('/personnel', data)
  },
  getPerson(id) {
    return api.get(`/personnel/${id}`)
  },
  updatePerson(id, data) {
    return api.put(`/personnel/${id}`, data)
  },
  deletePerson(id) {
    return api.delete(`/personnel/${id}`)
  },

  getSuppliers() {
    return api.get('/suppliers')
  },
  createSupplier(data) {
    return api.post('/suppliers', data)
  },
  getSupplier(id) {
    return api.get(`/suppliers/${id}`)
  },
  updateSupplier(id, data) {
    return api.put(`/suppliers/${id}`, data)
  },
  deleteSupplier(id) {
    return api.delete(`/suppliers/${id}`)
  },

  getEquipment() {
    return api.get('/equipment')
  },
  createEquipment(data) {
    return api.post('/equipment', data)
  },
  getEquipmentItem(id) {
    return api.get(`/equipment/${id}`)
  },
  updateEquipment(id, data) {
    return api.put(`/equipment/${id}`, data)
  },
  deleteEquipment(id) {
    return api.delete(`/equipment/${id}`)
  },

  search(keyword, category) {
    return api.get('/search', { params: { keyword, category } })
  }
}
