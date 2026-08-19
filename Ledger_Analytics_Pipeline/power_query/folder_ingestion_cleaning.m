let
  Source = Folder.Files("C:\Users\Ouss\Desktop\BI project\monthly_ledgers"),
  #"Filtered hidden files" = Table.SelectRows(Source, each [Attributes]?[Hidden]? <> true),
  #"Added custom" = let
    rootPath = Text.TrimEnd(Value.Metadata(Value.Type(#"Filtered hidden files"))[FileSystemTable.RootPath]?, "\"),
    combinePaths = (path1, path2) => Text.Combine({Text.TrimEnd(path1, "\"), path2}, "\"),
    getRelativePath = (path, relativeTo) => Text.Middle(path, Text.Length(relativeTo) + 1)
in
    Table.AddColumn(#"Filtered hidden files", "Relative Path", each getRelativePath(combinePaths([Folder Path], [Name]), rootPath), type text),
  #"Invoke custom function" = Table.AddColumn(#"Added custom", "Transform file", each #"Transform file"([Content])),
  #"Renamed columns" = Table.RenameColumns(#"Invoke custom function", {{"Relative Path", "Source.Name"}}),
  #"Removed other columns" = Table.SelectColumns(#"Renamed columns", {"Source.Name", "Transform file"}),
  #"Expanded table column" = Table.ExpandTableColumn(#"Removed other columns", "Transform file", Table.ColumnNames(#"Transform file"(#"Sample file"))),
  #"Changed column type" = Table.TransformColumnTypes(#"Expanded table column", {{"Column1", type text}, {"Column2", type text}, {"Column3", type text}, {"Column4", type text}, {"Column5", type text}, {"Column6", type text}, {"Column7", type text}, {"Column8", type text}, {"Column9", type text}}),
    #"Filtered Rows" = Table.SelectRows(#"Changed column type", each ([Column2] <> null)),
    #"Promoted Headers" = Table.PromoteHeaders(#"Filtered Rows", [PromoteAllScalars=true]),
    #"Changed Type" = Table.TransformColumnTypes(#"Promoted Headers",{{"Ledger_2025_01.xlsx", type text}, {"Date", type text}, {"Product_ID", type text}, {"Product_Name", type text}, {"Category", type text}, {"Town_ID", type text}, {"Town_Name", type text}, {"Region", type text}, {"Channel_ID", type text}, {"Channel_Name", type text}, {"Units_Sold", type any}, {"Unit_Price", type any}, {"Total_Revenue", type any}}),
    #"Filtered Rows1" = Table.SelectRows(#"Changed Type", each ([Date] <> "Date")),
    #"Changed Type1" = Table.TransformColumnTypes(#"Filtered Rows1",{{"Date", type date}, {"Product_ID", type text}, {"Product_Name", type text}, {"Category", type text}, {"Town_ID", type text}, {"Town_Name", type text}, {"Region", type text}, {"Channel_ID", type text}, {"Channel_Name", type text}, {"Units_Sold", Int64.Type}, {"Unit_Price", Currency.Type}, {"Total_Revenue", Currency.Type}}),
    #"Removed Columns" = Table.RemoveColumns(#"Changed Type1",{"Ledger_2025_01.xlsx"})
in
    #"Removed Columns"