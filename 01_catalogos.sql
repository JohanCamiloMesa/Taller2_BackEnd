INSERT INTO Pais (nombre,codigo_iso) VALUES
('Argentina','AR'),('Colombia','CO'),('México','MX'),('Perú','PE'),('España','ES');
INSERT INTO Ciudad (nombre,id_pais) VALUES
('Buenos Aires',1),('Córdoba',1),('Rosario',1),('Bogotá',2),('Medellín',2),
('Ciudad de México',3),('Guadalajara',3),('Lima',4),('Arequipa',4),('Madrid',5),('Barcelona',5);
INSERT INTO Sede (nombre,direccion,id_ciudad) VALUES
('Sede Central BA','Av. Corrientes 123',1),
('Sede Córdoba','Bv. San Juan 456',2),
('Sede Bogotá','Calle 100 7-21',4),
('Sede CDMX','Paseo de la Reforma 222',6),
('Sede Guadalajara','Av. Chapultepec 234',7),
('Sede Lima','Av. Larco 345',8),
('Sede Madrid','Calle de Alcalá 101',10);
INSERT INTO Tipo_Moneda (nombre,codigo,simbolo) VALUES
('Peso Argentino','ARS','$'),('Peso Colombiano','COP','$'),
('Peso Mexicano','MXN','$'),('Sol Peruano','PEN','S/'),('Euro','EUR','€');
INSERT INTO Producto (nombre,tipo,descripcion,id_moneda) VALUES
('Cuenta Corriente ARS','cuenta corriente','Cuenta Argentina',1),
('Caja de Ahorro ARS','cuenta ahorro','Ahorro Argentina',1),
('Cuenta Corriente COP','cuenta corriente','Cuenta Colombia',2),
('Caja de Ahorro COP','cuenta ahorro','Ahorro Colombia',2),
('Cuenta Corriente MXN','cuenta corriente','Cuenta México',3),
('Caja de Ahorro MXN','cuenta ahorro','Ahorro México',3),
('Cuenta Corriente PEN','cuenta corriente','Cuenta Perú',4),
('Caja de Ahorro PEN','cuenta ahorro','Ahorro Perú',4),
('Cuenta Corriente EUR','cuenta corriente','Cuenta España',5),
('Caja de Ahorro EUR','cuenta ahorro','Ahorro España',5);