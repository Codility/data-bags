const cache = {};

const idPrefix = 'data-bag-';


export default function getDataBag(name) {
  const cacheId = `$${name}`;
  const elementId = `${idPrefix}${name}`;

  if (!cache.hasOwnProperty(cacheId)) {
    const element = document.getElementById(elementId);

    if (!element) {
      throw new Error(`No such data bag: ${name}`);
    } else {
      cache[cacheId] = JSON.parse(element.textContent);
    }
  }

  return cache[cacheId];
}
