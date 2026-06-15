import api from './index'

export const authAPI = {
  register(data) {
    return api.post('/auth/register', data)
  },
  login(data) {
    return api.post('/auth/login', data)
  },
  getMe() {
    return api.get('/auth/me')
  }
}

export const buildingsAPI = {
  getList(params = {}) {
    return api.get('/buildings', { params })
  },
  getHot(limit = 10) {
    return api.get('/buildings/hot', { params: { limit } })
  },
  getById(id) {
    return api.get(`/buildings/${id}`)
  },
  create(data) {
    return api.post('/buildings', data)
  },
  update(id, data) {
    return api.put(`/buildings/${id}`, data)
  },
  delete(id) {
    return api.delete(`/buildings/${id}`)
  },
  getTypes() {
    return api.get('/buildings/type/list')
  },
  getHazards(id) {
    return api.get(`/buildings/${id}/hazards`)
  },
  addHazard(id, data) {
    return api.post(`/buildings/${id}/hazards`, data)
  }
}

export const mediaAPI = {
  uploadPhoto(buildingId, file, caption = '') {
    const formData = new FormData()
    formData.append('building_id', buildingId)
    formData.append('caption', caption)
    formData.append('file', file)
    return api.post('/media/photos', formData, {
      headers: { 'Content-Type': 'multipart/form-data' }
    })
  },
  deletePhoto(id) {
    return api.delete(`/media/photos/${id}`)
  },
  uploadVideo(buildingId, file, title = '', description = '') {
    const formData = new FormData()
    formData.append('building_id', buildingId)
    formData.append('title', title)
    formData.append('description', description)
    formData.append('file', file)
    return api.post('/media/videos', formData, {
      headers: { 'Content-Type': 'multipart/form-data' }
    })
  },
  deleteVideo(id) {
    return api.delete(`/media/videos/${id}`)
  }
}

export const commentsAPI = {
  getByBuilding(buildingId, page = 1, pageSize = 20) {
    return api.get(`/comments/building/${buildingId}`, {
      params: { page, page_size: pageSize }
    })
  },
  create(buildingId, data) {
    return api.post(`/comments/building/${buildingId}`, data)
  },
  like(id) {
    return api.post(`/comments/${id}/like`)
  },
  delete(id) {
    return api.delete(`/comments/${id}`)
  }
}

export const routesAPI = {
  getList(page = 1, pageSize = 20) {
    return api.get('/routes', { params: { page, page_size: pageSize } })
  },
  getById(id) {
    return api.get(`/routes/${id}`)
  },
  create(data) {
    return api.post('/routes', data)
  },
  delete(id) {
    return api.delete(`/routes/${id}`)
  }
}

export const statsAPI = {
  getStats(days = null) {
    const params = days ? { days } : {}
    return api.get('/statistics', { params })
  },
  getTimeseries(days = null) {
    const params = days ? { days } : {}
    return api.get('/statistics/timeseries', { params })
  },
  exportCSV(days = null) {
    const params = days ? { days } : {}
    return api.get('/statistics/export/csv', {
      params,
      responseType: 'blob'
    })
  }
}

export const timelineAPI = {
  getByBuilding(buildingId) {
    return api.get(`/timeline/building/${buildingId}`)
  },
  create(buildingId, data) {
    return api.post(`/timeline/building/${buildingId}`, data)
  },
  update(eventId, data) {
    return api.put(`/timeline/${eventId}`, data)
  },
  delete(eventId) {
    return api.delete(`/timeline/${eventId}`)
  }
}
