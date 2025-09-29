# panaram_generator
Генерация панорамы

### Запуск
```
docker build -t panorama-maker .
docker run -d -p 8060:8060 --name panorama panorama-maker
```

### Запрос из PHP

```
$ch = curl_init("http://localhost:8060/stitch");
$data = [
    'left' => new CURLFile('/path/to/left.jpg'),
    'center' => new CURLFile('/path/to/center.jpg'),
    'right' => new CURLFile('/path/to/right.jpg'),
];
curl_setopt($ch, CURLOPT_POST, true);
curl_setopt($ch, CURLOPT_POSTFIELDS, $data);
curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);

$result = curl_exec($ch);
file_put_contents("result.jpg", $result);
```
