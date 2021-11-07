import axios from 'axios'

const options = {
  // Gestion automatique du jeton avec une variable X-CSRFToken dans l entete
  // au lieu de la variable csrfmiddlewaretoken dans le body
  /*
  xsrfCookieName: 'csrftoken',
  xsrfHeaderName: 'X-CSRFToken',
  */
  withCredentials: false,
  headers: {
    'Access-Control-Allow-Origin': '*',
    'Content-Type': 'application/json',
    Accept: 'application/json'
  }
}

if (process.env.NODE_ENV === 'development') {
  options.withCredentials = true
}

async function get (url, params = {}) {
  return xhr('get', url, {}, params)
}

async function post (url, data = {}) {
  return xhr('post', url, data, {})
}

async function xhr (method = 'get', url, data = {}, params = {}) {
  options.method = method
  options.url = url
  options.data = data
  options.params = params
  try {
    const response = await axios(options)

    if (response.status === 200) {
      return response.data
    }
  } catch (error) {
    // TODO: Boite de dialogue global pour indiquer l erreur
    /*
    store.dispatch('common/showDialog', {
      title: 'Problème Internet',
      text: 'Impossible de se connecter à Internet',
    });
    */
    if (error.response) {
      /*
       * The request was made and the server responded with a
       * status code that falls out of the range of 2xx
       */
      console.log(error.response.status)
      console.log(error.response.headers)
      console.log(error.response.data)
    } else if (error.request) {
      /*
      * The request was made but no response was received, `error.request`
      * is an instance of XMLHttpRequest in the browser and an instance
      * of http.ClientRequest in Node.js
      */
      console.log(error.request)
    } else {
      // Something happened in setting up the request and triggered an Error
      console.log('Error', error.message)
    }
    console.log(error)
  }
  return false
}

export default {
  get,
  post,
  xhr
}
