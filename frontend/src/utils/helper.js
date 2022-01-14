import axios from "axios";
import { Link } from "react-router-dom";
import { useSelector } from "react-redux";
import { useStore } from "react-redux";

function stateEqual(state1, state2) {
  for(let key in state1) {
    if(state1[key] !== state2[key]) {
      return false;
    }
  }
  return true;
}

export function useMapSelector(mapFunc) {
  return useSelector(mapFunc, stateEqual);
}

export function useSliceSelector(namespace, keys) {
  let preKeys = namespace.split('/');
  return useMapSelector(globalState => {
      let pageStates = globalState;
      preKeys.forEach(preKey => pageStates = pageStates[preKey] || {});
      let selectedStates = [];
      keys.forEach(key => selectedStates.push(pageStates[key]));
      return selectedStates;
    }
  );
}

class SliceStore {
  constructor(namespace, store) {
    this._namespace = namespace;
    this._store = store;
  }

  dispatch(action) {
    this._store.dispatch({
      type: `${this._namespace}/${action.type}`, 
      payload: action.payload
    });
  }

  dispatchGlobal(action) {
    this._store.dispatch(action);
  }

  setState(payload) {
    this._store.dispatch({
      type: `${this._namespace}/setState`, 
      payload: payload
    });
  }

  getState() {
    let keys = this._namespace.split('/');
    let state = this._store.getState();
    keys.forEach(key => state = state[key] || {});
    return state; 
  }

  getGlobalState() {
    return this._store.getState();
  }
}

export function useSliceStore(namespace) {
  let store = useStore();
  return new SliceStore(namespace, store);
}

export function appendUrlParams(url, params) {
  if(!url.includes('?')) url += '?';
  for(let [key,value] of Object.entries(params || {})) {
    if(value !== null && value !== undefined){
      url += `&${key}=${encodeURIComponent(value)}`;
    }
  }
  return url;
}

export async function getOptions({url, params, getParams, labelField, valueField}) {
  params = params || {};
    
  if(getParams) {
    params = {...params, ...getParams()};
  }
  
  let result = await axios.get(appendUrlParams(url, params));
  let options = [];
  
  (result?.data??[]).forEach(item => options.push({
    ...item,
    label: item[labelField], 
    value: item[valueField]
  }));

  return options;
}

export function getLoadOptions({url, params, getParams, labelField, valueField}) {
  return (term, callback) => {
    params = params || {};
    
    if(getParams) {
      params = {...params, ...getParams()};
    }
    
    axios.get(appendUrlParams(url, {...params, term})).then(result => {
  
      let options = (result.data??[]).map(item => ({
        ...item,
        label: item[labelField], 
        value: item[valueField]
      }));
      
      if(options.length >= 30) {
        options.push({
          label: 'Gõ vào để tìm kiếm ...',
          value: '',
          isDisabled: true
        });
      }

      callback(options);
    });
  }
}

export function IconLink({title, icon, href, variant, size, className}) {
  return (
    <Link to={href ?? '#/'}>
      <a 
        className={`btn btn-${size ?? 'sm'} btn-${variant ?? 'primary'} ${className ?? ''}`}
      >
        <i className={`fas fa-${icon ?? ''} text-white-50`}></i> {title}
      </a>
    </Link>
  );
}

export function IconButton({title, icon, variant, size, className, type}) {
  return (
    <button 
      type={type} 
      className={`btn btn-${size ?? 'sm'} btn-${variant ?? 'primary'} ${className ?? ''}`}
    >
      <i className={`fas fa-${icon ?? ''} text-white-50`}></i> {title}
    </button>
  );
}

export function Spiner() {
  return(
    <div className="spinner-border" role="status">
      <span className="sr-only"></span>
    </div>
  );
}

export function serializeForm(fmt) {
  let formData = new FormData(fmt);
  let data = {};
  for(let pair of formData.entries()) {
    data[pair[0]] = pair[1]
  }
  return data;
}

export function copyObject(obj) {
  return {...obj};
}

export function copyArray(arr) {
  if(Array.isArray(arr)){
    return [...arr];
  }
}