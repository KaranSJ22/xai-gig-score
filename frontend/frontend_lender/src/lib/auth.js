export const saveToken = (token) => {
  localStorage.setItem('lender_token', token);
};

export const getToken = () => {
  return localStorage.getItem('lender_token');
};

export const removeToken = () => {
  localStorage.removeItem('lender_token');
};

export const isAuthenticated = () => {
  return !!getToken();
};
